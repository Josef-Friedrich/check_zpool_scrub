import argparse
from argparse import ArgumentParser

import check_zpool_scrub
from check_zpool_scrub import get_argparser
from tests.helper import run


class TestWithSubprocess:
    def test_help(self) -> None:
        process = run(["--help"])
        assert process.returncode == 3
        assert "usage: check_zpool_scrub" in process.stdout

    def test_version(self) -> None:
        process = run(
            ["--version"],
        )
        assert process.returncode == 3
        assert "check_zpool_scrub " + check_zpool_scrub.__version__ in process.stdout


parser: ArgumentParser = get_argparser()


def parse_args(*args: str) -> argparse.Namespace:
    return parser.parse_args(args)


class TestMethod:
    class TestWarning:
        def test_int(self) -> None:
            args = parse_args("--warning", "42")
            assert args.warning == 42

        def test_timespan(self) -> None:
            args = parse_args("--warning", "1s1m")
            assert args.warning == 61

    class TestCritical:
        def test_int(self) -> None:
            args = parse_args("--critical", "123")
            assert args.critical == 123

        def test_critical_timespan(self) -> None:
            args = parse_args("--critical", "1 min")
            assert args.critical == 60
