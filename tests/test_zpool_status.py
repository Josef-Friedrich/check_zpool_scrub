"""Test the class PoolScrubStatus"""

from datetime import datetime
from unittest.mock import Mock, patch

from freezegun import freeze_time

from check_zpool_scrub import PoolScrubStatus, _list_pools  # type: ignore


@patch("check_zpool_scrub.subprocess.check_output")
def test_list_pools(mock_run: Mock) -> None:
    mock_run.return_value = """
unknown_zpool
never_scrubbed_zpool
first_ok_zpool
last_ok_zpool
first_warning_zpool
last_warning_zpool
first_critical_zpool
"""
    pools = _list_pools()
    assert pools == [
        "unknown_zpool",
        "never_scrubbed_zpool",
        "first_ok_zpool",
        "last_ok_zpool",
        "first_warning_zpool",
        "last_warning_zpool",
        "first_critical_zpool",
    ]


def get_status(check_output: str) -> PoolScrubStatus:
    with patch("check_zpool_scrub.subprocess.check_output") as mock_run:
        mock_run.return_value = check_output
        return PoolScrubStatus("xxx")


@freeze_time("2026-02-19")
class TestInProgress:
    status: PoolScrubStatus = get_status("""
 pool: first_ok_zpool
state: ONLINE
 scan: scrub in progress since Thu Aug 17 10:25:48 2017
    9,12T scanned out of 9,48T at 1,90M/s, 55h33m to go
    0 repaired, 96,19% done
config:

    NAME                                 STATE     READ WRITE CKSUM
    data                                 ONLINE       0     0     0
    raidz1-0                             ONLINE       0     0     0
        ata-ST3000DM001-1CH166_Z1F324L3  ONLINE       0     0     0

errors: No known data errors'
""")

    def test_progress(self) -> None:
        assert self.status.progress == 0.9619

    def test_speed(self) -> None:
        assert self.status.speed == 1.9

    def test_last_scrub(self) -> None:
        assert self.status.last_scrub == datetime(2017, 8, 17, 10, 25, 48)

    def test_time_to_go(self) -> None:
        assert self.status.time_to_go == (55 * 60 + 33) * 60

    def test_last_scrub_interval(self) -> None:
        assert self.status.last_scrub_timespan == 268493652


@freeze_time("2026-02-19")
class TestFinished:
    status: PoolScrubStatus = get_status("""  pool: data
 state: ONLINE
  scan: scrub repaired 0 in 266h29m with 0 errors on Fri Jun 16 10:25:47 2017
config:

	NAME                                     STATE     READ WRITE CKSUM
	data                                     ONLINE       0     0     0
	  raidz1-0                               ONLINE       0     0     0
	    ata-TOSHIBA_MD04ACA400_9614KMR9FSAA  ONLINE       0     0     0

errors: No known data errors
""")

    def test_progress(self) -> None:
        assert self.status.progress is None

    def test_speed(self) -> None:
        assert self.status.speed is None

    def test_last_scrub(self) -> None:
        assert self.status.last_scrub == datetime(2017, 6, 16, 10, 25, 47)

    def test_time_to_go(self) -> None:
        assert self.status.time_to_go is None

    def test_last_scrub_interval(self) -> None:
        assert self.status.last_scrub_timespan == 273850453
