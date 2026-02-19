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
from typing import Optional, cast

import nagiosplugin

# from nagiosplugin.runtime import guarded

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
    def progress(self) -> float:
        """Grab the scrub progress from the 'zpool status' output.

        Percent 0 - 100

        A floating point number from 0 to 100 that represents the progress
        (for example ``85.3``)."""
        match = re.search(r"(\d+,\d+)% done", self.__zpool_status_output)
        if match is None:
            return 100.0
        progress = match[1]
        progress = progress.replace(",", ".")
        return float(progress)

    @property
    def speed(self) -> float:
        """MB per second."""
        match = re.search(r"at (\d+,\d+)M/s", self.__zpool_status_output)
        if match is None:
            return 0
        speed = match[1]
        speed = speed.replace(",", ".")
        return float(speed)

    @property
    def time_to_go(self) -> int:
        """Time to go in seconds.

        https://github.com/openzfs/zfs/blob/cdf89f413c72fb17107a2b830a86161a21c74f82/cmd/zpool/zpool_main.c#L10229"""
        match = re.search(r"(\d+)h(\d+)m to go\n", self.__zpool_status_output)
        if match is None:
            return 0
        return (int(match[1]) * 60 + int(match[2])) * 60

    @property
    def last_scrub(self) -> Optional[datetime]:
        match = re.search(
            "(canceled on|in progress since|errors on) (.*)\n",
            self.__zpool_status_output,
        )
        if match is None:
            return None

        return datetime.strptime(match[2], "%c")

    @property
    def last_scrub_interval(self) -> Optional[float]:
        """Time interval in seconds for last scrub."""
        if self.last_scrub is not None:
            return datetime.now().timestamp() - self.last_scrub.timestamp()
        return None


class PoolResource(nagiosplugin.Resource):
    pool: str

    def __init__(self, pool: str) -> None:
        self.pool = pool

    def probe(self) -> typing.Generator[nagiosplugin.Metric, typing.Any, None]:
        status = PoolScrubStatus(self.pool)

        yield nagiosplugin.Metric(f"{self.pool}_progress", status.progress)
        yield nagiosplugin.Metric(f"{self.pool}_speed", status.speed)
        yield nagiosplugin.Metric(f"{self.pool}_time_to_go", status.time_to_go)


class ScrubContext(nagiosplugin.Context):
    pass


def get_argparser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog="check_zpool_scrub",  # To get the right command name in the README.
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog, width=80
        ),  # noqa: E501
        description="Copyright (c) 2016-22 Josef Friedrich <josef@friedrich.rocks>\n"
        "\n"
        "Monitoring plugin to check how long ago the last ZFS scrub was performed.\n",  # noqa: E501
        epilog="Performance data:\n"
        "\n"
        "POOL is the name of the pool\n"
        "\n"
        " - POOL_last_ago\n"
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

    # https://github.com/monitoring-plugins/monitoring-plugin-guidelines/blob/main/monitoring_plugins_interface/02.Input.md
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (use up to 3 times).",
    )

    parser.add_argument(
        "-c",
        "--critical",
        help="Interval in seconds for critical state.",
    )

    parser.add_argument(
        "-p",
        "--pool",
        help="Name of the pool. If this option is omitted all pools are checked.",
    )

    parser.add_argument(
        "-s",
        "--short-description",
        help="Show a short description / summary.",
    )

    # https://github.com/monitoring-plugins/monitoring-plugin-guidelines/blob/main/monitoring_plugins_interface/02.Input.md
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
    )

    parser.add_argument(
        "-w",
        "--warning",
        help="Interval in seconds for warning state. Must be lower than -c.",
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="count",
        default=0,
        help="Increase debug verbosity (use up to 3 times): -D: info -DD: debug. -DDD verbose",
    )

    return parser


# @guarded(verbose=0)
def main(*args: str) -> None:
    global opts

    argv: list[str]
    if len(args) == 0:
        argv = sys.argv
    else:
        argv = list(args)
    opts = cast(OptionContainer, get_argparser().parse_args(argv))

    checks: list[typing.Union[nagiosplugin.Resource, nagiosplugin.Context]] = []

    pools = _list_pools()

    if opts.pool is not None:
        if opts.pool not in pools:
            raise ValueError(f"-p {opts.pool} is not in {pools}")
        checks.append(PoolResource(opts.pool))
    else:
        for pool in pools:
            checks.append(PoolResource(pool))

    check: nagiosplugin.Check = nagiosplugin.Check(*checks)
    check.name = "zpool_scrub"
    check.main(opts.verbose)


if __name__ == "__main__":
    main()
