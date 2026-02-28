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


def args(*args: str) -> argparse.Namespace:
    return parser.parse_args(args)


class TestMethod:
    class TestPool:
        def test_none(self) -> None:
            assert args().pool is None

        def test_long_option(self) -> None:
            assert args("--pool", "test-pool").pool == "test-pool"

        def test_short_option(self) -> None:
            assert args("-p", "test-pool").pool == "test-pool"

    class TestWarning:
        def test_int(self) -> None:
            assert args("--warning", "42").warning == 42

        def test_timespan(self) -> None:
            assert args("--warning", "1s1m").warning == 61

    class TestCritical:
        def test_int(self) -> None:
            assert args("--critical", "123").critical == 123

        def test_critical_timespan(self) -> None:
            assert args("--critical", "1 min").critical == 60

    class TestVerbose:
        def test_zero(self) -> None:
            assert args().verbose == 0

        def test_one(self) -> None:
            assert args("-v").verbose == 1

        def test_two(self) -> None:
            assert args("-vv").verbose == 2

        def test_three(self) -> None:
            assert args("-vvv").verbose == 3
