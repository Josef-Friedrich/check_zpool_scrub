#! /usr/bin/env python3

import argparse
from argparse import ArgumentParser
from nagiosplugin.runtime import guarded
from typing import cast


class OptionContainer:
    pass


opts: OptionContainer = OptionContainer()


def get_argparser() -> ArgumentParser:
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="check_zpool_scrub",  # To get the right command name in the README.
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
        help="Show the version number.",
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
