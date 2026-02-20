from __future__ import annotations

import io
import subprocess
import typing
from contextlib import redirect_stderr, redirect_stdout
from unittest import mock
from unittest.mock import Mock

from freezegun import freeze_time

import check_zpool_scrub


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
    time: str = "2017-08-17 10:25:48",
) -> MockResult:
    def perform_subprocess_output(args: list[str], **kwargs: typing.Any) -> str:
        command: str = " ".join(args)

        if command == "zpool status unknown_zpool":
            return ""

        elif command == "zpool status first_ok_zpool":
            return """  pool: first_ok_zpool
 state: ONLINE
  scan: scrub in progress since Thu Aug 17 10:25:48 2017
    9,12T scanned out of 9,48T at 1,90M/s, 55h33m to go
    0 repaired, 96,19% done
config:

	NAME                                 STATE     READ WRITE CKSUM
	data                                 ONLINE       0     0     0
	  raidz1-0                           ONLINE       0     0     0
	    ata-ST3000DM001-1CH166_Z1F324L3  ONLINE       0     0     0

errors: No known data errors
"""
        elif command == "zpool status last_ok_zpool":
            return """  pool: first_ok_zpool
 state: ONLINE
  scan: scrub in progress since Mon Jul 17 10:25:48 2017
    9,12T scanned out of 9,48T at 1,90M/s, 55h33m to go
    0 repaired, 96,19% done
config:

	NAME                                 STATE     READ WRITE CKSUM
	data                                 ONLINE       0     0     0
	  raidz1-0                           ONLINE       0     0     0
	    ata-ST3000DM001-1CH166_Z1F324L3  ONLINE       0     0     0

errors: No known data errors
"""
        elif command == "zpool status first_warning_zpool":
            return """  pool: data
 state: ONLINE
  scan: scrub in progress since Mon Jul 17 10:25:47 2017
    7,34T scanned out of 10,1T at 57,4M/s, 14h12m to go
    0 repaired, 72,38% done
config:

	NAME                                          STATE     READ WRITE CKSUM
	data                                          ONLINE       0     0     0
	  raidz1-0                                    ONLINE       0     0     0
	    ata-WDC_WD30EZRX-00SPEB0_WD-WCC4EHYCFSFV  ONLINE       0     0     0

errors: No known data errors
"""
        elif command == "zpool status last_warning_zpool":
            return """  pool: data
 state: ONLINE
  scan: scrub in progress since Fri Jun 16 10:25:48 2017
    7,34T scanned out of 10,1T at 57,4M/s, 14h12m to go
    0 repaired, 72,38% done
config:

	NAME                                          STATE     READ WRITE CKSUM
	data                                          ONLINE       0     0     0
	  raidz1-0                                    ONLINE       0     0     0
	    ata-WDC_WD30EZRX-00SPEB0_WD-WCC4EHYCFSFV  ONLINE       0     0     0

errors: No known data errors

"""
        elif command == "zpool status first_critical_zpool":
            return """  pool: data
 state: ONLINE
  scan: scrub repaired 0 in 266h29m with 0 errors on Fri Jun 16 10:25:47 2017
config:

	NAME                                     STATE     READ WRITE CKSUM
	data                                     ONLINE       0     0     0
	  raidz1-0                               ONLINE       0     0     0
	    ata-TOSHIBA_MD04ACA400_9614KMR9FSAA  ONLINE       0     0     0

errors: No known data errors
"""
        elif command == "zpool status never_scrubbed_zpool":
            return """  pool: never_scrubbed_zpool
 state: ONLINE
  scan: none requested
config:

	NAME           STATE     READ WRITE CKSUM
	system         ONLINE       0     0     0
	  mirror-0     ONLINE       0     0     0
	    gpt/disk0  ONLINE       0     0     0
	    ada1p3     ONLINE       0     0     0

errors: No known data errors
"""
        # see https://github.com/Josef-Friedrich/check_zpool_scrub/issues/11
        elif command == "zpool status days_to_go":
            return """  pool: days_to_go
 state: ONLINE
  scan: scrub in progress since Thu Aug 17 10:25:48 2017
        461G scanned at 120M/s, 258G issued at 67.2M/s, 496G total
        0B repaired, 52.05% done, 0 days 01:01:21 to go
config:

        NAME                                       STATE     READ WRITE CKSUM
        zfsdata                                    ONLINE       0     0     0
          mirror-0                                ONLINE       0     0     0
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)

"""
        # https://github.com/Josef-Friedrich/check_zpool_scrub/issues/11#issuecomment-850798342

        elif command == "zpool status time_to_go_colons":
            return """  pool: time_to_go_colons
 state: ONLINE
  scan: scrub in progress since Thu Aug 17 10:25:48 2017
        461G scanned at 120M/s, 258G issued at 67.2M/s, 496G total
        0B repaired, 52.05% done, 01:01:21 to go
config:

        NAME                                       STATE     READ WRITE CKSUM
        zfsdata                                    ONLINE       0     0     0
          mirror-0                                ONLINE       0     0     0
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)

"""
        elif command == "zpool list -H -o name":
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

    file_stdout: io.StringIO = io.StringIO()
    file_stderr: io.StringIO = io.StringIO()

    with (
        mock.patch("sys.exit") as sys_exit,
        mock.patch(
            "check_zpool_scrub.subprocess.check_output",
            side_effect=perform_subprocess_output,
        ),
        mock.patch("sys.argv", argv),
        freeze_time(time),
        redirect_stdout(file_stdout),
        redirect_stderr(file_stderr),
    ):
        check_zpool_scrub.main()

    return MockResult(
        sys_exit_mock=sys_exit,
        stdout=file_stdout.getvalue(),
        stderr=file_stderr.getvalue(),
    )
