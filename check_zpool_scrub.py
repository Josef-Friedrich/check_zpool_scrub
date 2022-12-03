#! /usr/bin/env python3

import argparse
from typing import cast

from nagiosplugin.runtime import guarded

__version__: str = "2.0"


class OptionContainer:
    pass


opts: OptionContainer = OptionContainer()


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
