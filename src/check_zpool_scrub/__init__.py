#! /usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import typing
from datetime import datetime
from importlib import metadata
from typing import Optional, cast

from mplugin import (
    TIMESPAN_FORMAT_HELP,
    Check,
    Context,
    Metric,
    Performance,
    Resource,
    Result,
    guarded,
    log,
    setup_argparser,
    timespan,
)

__version__: str = metadata.version("check_zpool_scrub")


class OptionContainer:
    pool: Optional[str]
    debug: int
    verbose: int
    warning: int
    critical: int


opts: OptionContainer = OptionContainer()


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
    log.debug("Output from %s: %s", "zpool list -H -o name", pools)
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
        log.debug("Output from %s: %s", "zpool status", self.__zpool_status_output)

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

        if metric.value is None:
            return self.unknown(f"The pool “{r.pool}” has never had a scrub.")

        if metric.value > opts.critical:
            return self.critical(
                metric=metric,
                hint=f"Pool “{r.pool}”: {metric.value} >= {opts.critical}",
            )

        if metric.value > opts.warning:
            return self.warning(
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
        "'zpool status POOL'.\n" + TIMESPAN_FORMAT_HELP,
        verbose=True,
    )

    parser.add_argument(
        "-p",
        "--pool",
        help="Name of the pool. If this option is omitted all pools are checked.",
    )

    parser.add_argument(
        "-w",
        "--warning",
        # 1 month 60*60*24*31
        metavar="TIMESPAN",
        default=2678400,
        help="Interval in seconds for warning state. See timespan format specification below. Must be lower than -c.",
        type=timespan,
    )

    parser.add_argument(
        "-c",
        "--critical",
        # 2 month 60*60*24*31*2,
        metavar="TIMESPAN",
        default=5356800,
        help="Interval in seconds for critical state. See timespan format specification below.",
        type=timespan,
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Increase debug verbosity (use up to 3 times): -D: info -DD: debug. -DDD verbose",
    )

    return parser


@guarded(verbose=0)
def main() -> None:
    global opts

    opts = cast(OptionContainer, get_argparser().parse_args())

    if opts.warning > opts.critical:
        raise ValueError(
            f"-w SECONDS must be smaller than -c SECONDS. -w {opts.warning} > -c {opts.critical}"
        )

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
    check.main(verbose=opts.verbose)


if __name__ == "__main__":
    main()
