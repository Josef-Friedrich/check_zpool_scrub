#! /usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
from datetime import datetime
from importlib import metadata
from typing import Optional, cast

import nagiosplugin

# from nagiosplugin.runtime import guarded

__version__: str = metadata.version("check_zpool_scrub")


class OptionContainer:
    pass


opts: OptionContainer = OptionContainer()


class PoolStatus:
    pool: str

    __zpool_status_output: str

    last_ago: int
    """Time interval in seconds for last scrub."""

    time: int
    """Time to go in seconds."""

    def __init__(self, pool: str) -> None:
        self.pool = pool
        # https://github.com/openzfs/zfs/blob/master/cmd/zpool/zpool_main.c
        self.__zpool_status_output = subprocess.check_output(
            ["zpool", "status", pool], encoding="UTF-8"
        )

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
    def since(self) -> Optional[datetime]:
        match = re.search(
            "(canceled on|in progress since|errors on) (.*)\n",
            self.__zpool_status_output,
        )
        if match is None:
            return None

        return datetime.strptime(match[2], "%c")


class StatusResource(nagiosplugin.Resource):
    name = "status"

    dataset: str

    def __init__(self, dataset: str) -> None:
        self.dataset = dataset

    def probe(self) -> nagiosplugin.Metric:

        output = subprocess.check_output(
            ["zpool", "status", self.dataset], encoding="UTF-8"
        )

        return nagiosplugin.Metric("snapshot_count", output)


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
        " - POOL_time\n"
        "    Time to go in seconds.\n"
        "\n"
        "Details about the implementation of this monitoring plugin:\n"
        "\n"
        "This monitoring plugin grabs the last scrub date from the command\n"
        "'zpool status POOL'.\n",
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

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="%(prog)s {}".format(__version__),
    )

    parser.add_argument(
        "-w",
        "--warning",
        help="Interval in seconds for warning state. Must be lower than -c.",
    )

    return parser


# @guarded(verbose=0)
def main():
    pass
    global opts
    opts = cast(OptionContainer, get_argparser().parse_args())


if __name__ == "__main__":
    main()
