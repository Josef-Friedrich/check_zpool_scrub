from __future__ import annotations

import importlib
import io
import subprocess
import typing
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock
from unittest.mock import Mock

from freezegun import freeze_time


def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["check_zpool_scrub"] + args,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class MockResult:
    """A class to collect all results of a mocked execution of the main
    function."""

    __sys_exit: Mock
    __stdout: str | None
    __stderr: str | None

    def __init__(self, sys_exit_mock: Mock, stdout: str, stderr: str) -> None:
        self.__sys_exit = sys_exit_mock
        self.__stdout = stdout
        self.__stderr = stderr

    @property
    def exitcode(self) -> int:
        """The captured exit code"""
        return int(self.__sys_exit.call_args[0][0])

    @property
    def stdout(self) -> str | None:
        """The function ``redirect_stdout()`` is used to capture the ``stdout``
        output."""
        if self.__stdout:
            return self.__stdout
        return None

    @property
    def stderr(self) -> str | None:
        """The function ``redirect_stderr()`` is used to capture the ``stderr``
        output."""
        if self.__stderr:
            return self.__stderr
        return None

    @property
    def output(self) -> str:
        """A combined string of the captured stderr, stdout  and the print
        calls. Somehow the whole stdout couldn’t be read. The help text could
        be read, but not the plugin output using the function
        ``redirect_stdout()``."""
        out: str = ""

        if self.__stderr:
            out += self.__stderr

        if self.__stdout:
            out += self.__stdout

        return out

    @property
    def first_line(self) -> str | None:
        """The first line of the output without a newline break at the
        end as a string.
        """
        if self.output:
            return self.output.split("\n", 1)[0]
        return None


def execute_main(
    argv: list[str] = ["check_zpool_scrub"],
    time: str = "2017-09-01 10:55:34",
) -> MockResult:
    def perform_subprocess_run_side_effect(
        args: list[str], **kwargs: typing.Any
    ) -> str:
        command: str = " ".join(args)

        if command == "zpool list -H -o name":
            return """unknown_zpool
never_scrubbed_zpool
first_ok_zpool
last_ok_zpool
first_warning_zpool
last_warning_zpool
first_critical_zpool"""

        return ""

    if not argv or argv[0] != "check_zpool_scrub":
        argv.insert(0, "check_zpool_scrub")

    with (
        mock.patch("sys.exit") as sys_exit,
        mock.patch(
            "check_zpool_scrub.subprocess.check_output",
            side_effect=perform_subprocess_run_side_effect,
        ),
        mock.patch("sys.argv", argv),
        freeze_time(time),
    ):
        file_stdout: io.StringIO = io.StringIO()
        file_stderr: io.StringIO = io.StringIO()
        with redirect_stdout(file_stdout), redirect_stderr(file_stderr):
            importlib.import_module("check_zpool_scrub").main()

    return MockResult(
        sys_exit_mock=sys_exit,
        stdout=file_stdout.getvalue(),
        stderr=file_stderr.getvalue(),
    )
