#! /usr/bin/env python3

from __future__ import annotations

import argparse
import logging
import re
import subprocess
import sys
import typing
from datetime import datetime
from importlib import metadata
from typing import Any, Optional, Sequence, Union, cast

from mplugin import (
    Check,
    Context,
    Metric,
    Performance,
    Resource,
    Result,
    guarded,
    setup_argparser,
)

__version__: str = metadata.version("check_zpool_scrub")


class OptionContainer:
    pool: Optional[str]
    debug: int
    verbose: int
    warning: int
    critical: int


opts: OptionContainer = OptionContainer()


class Logger:
    """A wrapper around the Python logging module with 3 debug logging levels.

    1. ``-d``: info
    2. ``-dd``: debug
    3. ``-ddd``: verbose
    """

    __logger: logging.Logger

    __BLUE = "\x1b[0;34m"
    __PURPLE = "\x1b[0;35m"
    __CYAN = "\x1b[0;36m"
    __RESET = "\x1b[0m"

    __INFO = logging.INFO
    __DEBUG = logging.DEBUG
    __VERBOSE = 5

    def __init__(self) -> None:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(message)s"))
        logging.basicConfig(handlers=[handler])
        self.__logger = logging.getLogger(__name__)

    def set_level(self, level: int) -> None:
        # NOTSET=0
        # custom level: VERBOSE=5
        # DEBUG=10
        # INFO=20
        # WARN=30
        # ERROR=40
        # CRITICAL=50
        if level == 1:
            self.__logger.setLevel(logging.INFO)
        elif level == 2:
            self.__logger.setLevel(logging.DEBUG)
        elif level > 2:
            self.__logger.setLevel(5)

    def __log(self, level: int, color: str, msg: str, *args: object) -> None:
        a: list[str] = []
        for arg in args:
            a.append(color + str(arg) + self.__RESET)
        self.__logger.log(level, msg, *a)

    def info(self, msg: str, *args: object) -> None:
        """Log on debug level ``1``: ``-d``.

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__INFO, self.__BLUE, msg, *args)

    def debug(self, msg: str, *args: object) -> None:
        """Log on debug level ``2``: ``-dd``.

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__DEBUG, self.__PURPLE, msg, *args)

    def verbose(self, msg: str, *args: object) -> None:
        """Log on debug level ``3``: ``-ddd``

        :param msg: A message format string. Note that this means that you can
            use keywords in the format string, together with a single
            dictionary argument. No ``%`` formatting operation is performed on
            ``msg`` when no args are supplied.
        :param args: The arguments which are merged into ``msg`` using the
            string formatting operator.
        """
        self.__log(self.__VERBOSE, self.__CYAN, msg, *args)

    def show_levels(self) -> None:
        msg = "log level %s (%s): %s"
        self.info(msg, 1, "info", "-d")
        self.debug(msg, 2, "debug", "-dd")
        self.verbose(msg, 3, "verbose", "-ddd")


logger = Logger()


def _list_pools() -> list[str]:
    pools: list[str] = (
        subprocess.check_output(
            [
                "zpool",
                "list",
                # -H Scripted mode.  Do not display headers, and separate fields by a single tab instead of arbitrary space.
                "-H",
                # -o property Comma-separated list of properties to display.  See the zpoolprops(7) manual page for a list of valid properties.  The default list is name, size, allocated, free, checkpoint, expandsize, fragmentation, capacity, dedupratio, health, altroot.
                "-o",
                "name",
            ],
            encoding="utf-8",
        )
        .strip()
        .splitlines()
    )
    logger.verbose("Output from %s: %s", "zpool list -H -o name", pools)
    return pools


class PoolScrubStatus:
    pool: str

    __zpool_status_output: str

    def __init__(self, pool: str) -> None:
        self.pool = pool
        # https://github.com/openzfs/zfs/blob/master/cmd/zpool/zpool_main.c
        self.__zpool_status_output = subprocess.check_output(
            ["zpool", "status", pool], encoding="UTF-8"
        )
        logger.verbose("Output from %s: %s", "zpool status", self.__zpool_status_output)

    @property
    def progress(self) -> Optional[float]:
        """The scrub progress from the ``zpool status`` output.

        :return: A floating point number from ``0`` to ``1`` that represents the progress
        (for example ``0.853``)."""
        match = re.search(r"(\d+,\d+)% done", self.__zpool_status_output)
        if match is None:
            return None
        progress = match[1]
        progress = progress.replace(",", ".")
        return float(progress) / 100

    @property
    def speed(self) -> Optional[float]:
        """MB per second."""
        match = re.search(r"at (\d+,\d+)M/s", self.__zpool_status_output)
        if match is None:
            return None
        speed = match[1]
        speed = speed.replace(",", ".")
        return float(speed)

    @property
    def time_to_go(self) -> Optional[int]:
        """Time to go in seconds.

        https://github.com/openzfs/zfs/blob/cdf89f413c72fb17107a2b830a86161a21c74f82/cmd/zpool/zpool_main.c#L10229"""
        match = re.search(r"(\d+)h(\d+)m to go\n", self.__zpool_status_output)
        if match is None:
            return None
        return (int(match[1]) * 60 + int(match[2])) * 60

    @property
    def last_scrub(self) -> Optional[datetime]:
        match = re.search(
            r"(canceled on|in progress since|errors on) (.*)\n",
            self.__zpool_status_output,
        )
        if match is None:
            return None

        return datetime.strptime(match[2], "%c")

    @property
    def last_scrub_timespan(self) -> Optional[int]:
        """Time interval in seconds for last scrub."""
        if self.last_scrub is not None:
            return round(datetime.now().timestamp() - self.last_scrub.timestamp())
        return None


class PoolResource(Resource):
    pool: str

    def __init__(self, pool: str) -> None:
        self.pool = pool

    def probe(self) -> typing.Generator[Metric, typing.Any, None]:
        status = PoolScrubStatus(self.pool)
        yield Metric(f"{self.pool}: progress", status.progress, context="progress")
        yield Metric(f"{self.pool}: speed", status.speed, context="speed")
        yield Metric(
            f"{self.pool}: time_to_go", status.time_to_go, context="time_to_go"
        )
        yield Metric(
            f"{self.pool}: last_scrub_timestamp",
            status.last_scrub,
            context="last_scrub_timestamp",
        )
        yield Metric(
            f"{self.pool}: last_scrub_timespan",
            status.last_scrub_timespan,
            context="last_scrub_timespan",
        )


class ProgressContext(Context):
    def __init__(self) -> None:
        super().__init__("progress")

    def performance(self, metric: Metric, resource: Resource) -> Optional[Performance]:
        if metric.value is None:
            return None
        return Performance(label=metric.name, value=metric.value * 100, uom="%")


class SpeedContext(Context):
    def __init__(self) -> None:
        super().__init__("speed")

    def performance(self, metric: Metric, resource: Resource) -> Optional[Performance]:
        if metric.value is None:
            return None
        return Performance(label=metric.name, value=metric.value, uom="m/s")


class TimeToGoContext(Context):
    def __init__(self) -> None:
        super().__init__("time_to_go")

    def performance(self, metric: Metric, resource: Resource) -> Optional[Performance]:
        if metric.value is None:
            return None
        return Performance(label=metric.name, value=metric.value, uom="s")


class LastScrubTimestampContext(Context):
    def __init__(self) -> None:
        super().__init__("last_scrub_timestamp")

    def performance(self, metric: Metric, resource: Resource) -> Optional[Performance]:
        if metric.value is None:
            return None
        return Performance(label=metric.name, value=round(metric.value.timestamp()))


class LastScrubTimespanContext(Context):
    def __init__(self) -> None:
        super().__init__("last_scrub_timespan")

    def evaluate(self, metric: Metric, resource: Resource) -> Result:
        r = cast(PoolResource, resource)
        if metric.value > opts.critical:
            return self.critical(
                metric=metric,
                hint=f"Pool “{r.pool}”: {metric.value} >= {opts.critical}",
            )
        if metric.value > opts.warning:
            return self.warn(
                metric=metric,
                hint=f"Pool “{r.pool}”: {metric.value} >= {opts.critical}",
            )
        return self.ok(
            metric=metric,
            hint=f"Pool “{r.pool}”: {metric.value} < {opts.warning}",
        )

    def performance(self, metric: Metric, resource: Resource) -> Optional[Performance]:
        if metric.value is None:
            return None
        return Performance(label=metric.name, value=metric.value, uom="s")


class CustomArgumentParser(argparse.ArgumentParser):
    """To get --help and --version exit with 3"""

    def exit(self, status: int = 3, message: Optional[str] = None) -> typing.NoReturn:
        if message:
            self._print_message(message, sys.stderr)
        sys.exit(status)

    # systemd.time(7)
    #    •   usec, us, μs
    #    •   msec, ms
    #    •   seconds, second, sec, s
    #    •   minutes, minute, min, m
    #    •   hours, hour, hr, h
    #    •   days, day, d
    #    •   weeks, week, w
    #    •   months, month, M (defined as 30.44 days)
    #    •   years, year, y (defined as 365.25 days)


def _convert_timespan_to_seconds(fmt_timespan: typing.Union[str, int, float]) -> int:
    """Convert a timespan format string to seconds. Take a look at the
    systemd `time-util.c
    <https://github.com/systemd/systemd/blob/master/src/basic/time-util.c>`_
    source code.

    :param fmt_timespan: for example ``2.345s`` or ``3min 45.234s`` or
    ``34min left`` or ``2 months 8 days``

    :return: The seconds
    """

    # A int or a float encoded as string without an extension
    try:
        fmt_timespan = float(fmt_timespan)
    except ValueError:
        pass

    if isinstance(fmt_timespan, int) or isinstance(fmt_timespan, float):
        return round(fmt_timespan)

    # Remove all whitespaces
    fmt_timespan = re.sub(r"\s+", "", fmt_timespan)

    replacements: list[tuple[list[str], str]] = [
        (["years", "year"], "y"),
        (["months", "month"], "M"),
        (["weeks", "week"], "w"),
        (["days", "day"], "d"),
        (["hours", "hour", "hr"], "h"),
        (["minutes", "minute", "min"], "m"),
        (["seconds", "second", "sec"], "s"),
        # (["msec"], "ms"),
        # (["usec", "μ"], "us"),
    ]

    for replacement in replacements:
        for r in replacement[0]:
            fmt_timespan = fmt_timespan.replace(r, replacement[1])

    # Add a whitespace after the units
    fmt_timespan = re.sub(r"([a-zA-Z]+)", r"\1 ", fmt_timespan)

    seconds: dict[str, float] = {
        "y": 31557600,  # 365.25 days
        "M": 2630016,  # 30.44 days
        "w": 604800,  # 7 * 24 * 60 * 60
        "d": 86400,  # 24 * 60 * 60
        "h": 3600,  # 60 * 60
        "m": 60,
        "s": 1,
        # "ms": 0.001,
    }
    result: float = 0
    # Split on the whitespaces
    for span in fmt_timespan.split():
        match = re.search(r"([\d\.]+)([a-zA-Z]+)", span)
        if match:
            value = match.group(1)
            unit = match.group(2)
            result += float(value) * seconds[unit]
    return round(result)


def get_argparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = setup_argparser(
        name="zpool_scrub",
        version=__version__,
        license="MIT",
        repository="https://github.com/Josef-Friedrich/check_zpool_scrub",
        copyright=f"Copyright (c) 2016-{datetime.now().year} Josef Friedrich <josef@friedrich.rocks>",
        description="Monitoring plugin to check how long ago the last ZFS scrub was performed.",
        epilog="Performance data:\n"
        "\n"
        "POOL is the name of the pool\n"
        "\n"
        " - POOL_last_scrub\n"
        "    Time interval in seconds for last scrub.\n"
        " - POOL_progress\n"
        "    Percent 0 - 100\n"
        " - POOL_speed\n"
        "    MB per second.\n"
        " - POOL_time_to_go\n"
        "    Time to go in seconds.\n"
        "\n"
        "Details about the implementation of this monitoring plugin:\n"
        "\n"
        "This monitoring plugin grabs the last scrub date from the command\n"
        "'zpool status POOL'.\n",
    )

    class TimeSpanAction(argparse.Action):
        def __init__(
            self,
            option_strings: list[str],
            dest: str,
            nargs: Optional[str] = None,
            **kwargs: Any,
        ) -> None:
            if nargs is not None:
                raise ValueError("nargs not allowed")
            super().__init__(option_strings, dest, **kwargs)

        def __call__(
            self,
            parser: argparse.ArgumentParser,
            namespace: argparse.Namespace,
            values: Optional[Union[str, Sequence[Any]]],
            option_string: Optional[str] = None,
        ) -> None:
            if not isinstance(values, str):
                raise ValueError("Only strings are allowed")
            setattr(namespace, self.dest, _convert_timespan_to_seconds(values))

    # https://github.com/monitoring-plugins/monitoring-plugin-guidelines/blob/main/monitoring_plugins_interface/02.Input.md
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (use up to 3 times).",
    )

    parser.add_argument(
        "-w",
        "--warning",
        # 1 month 60*60*24*31
        default=2678400,
        help="Interval in seconds for warning state. Must be lower than -c.",
        action=TimeSpanAction,
    )

    parser.add_argument(
        "-c",
        "--critical",
        # 2 month 60*60*24*31*2
        default=5356800,
        help="Interval in seconds for critical state.",
        action=TimeSpanAction,
    )

    parser.add_argument(
        "-p",
        "--pool",
        help="Name of the pool. If this option is omitted all pools are checked.",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Increase debug verbosity (use up to 3 times): -D: info -DD: debug. -DDD verbose",
    )

    return parser


@guarded(verbose=0)  # type: ignore
def main() -> None:
    global opts

    opts = cast(OptionContainer, get_argparser().parse_args())

    checks: list[typing.Union[Resource, Context]] = [
        ProgressContext(),
        SpeedContext(),
        TimeToGoContext(),
        LastScrubTimestampContext(),
        LastScrubTimespanContext(),
    ]

    pools = _list_pools()

    if opts.pool is not None:
        if opts.pool not in pools:
            formatted_pools = map(lambda pool: f"'{pool}'", pools)
            raise ValueError(
                f"Unknown pool '{opts.pool}'. Available pools: {', '.join(formatted_pools)}"
            )
        checks.append(PoolResource(opts.pool))
    else:
        for pool in pools:
            checks.append(PoolResource(pool))

    check: Check = Check(*checks)
    check.name = "zpool_scrub"
    check.main(opts.verbose)


if __name__ == "__main__":
    main()
