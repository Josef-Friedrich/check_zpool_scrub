from datetime import datetime
from unittest.mock import Mock, patch

from check_zpool_scrub import PoolStatus


@patch("check_zpool_scrub.subprocess.check_output")
def test_first_ok_zpool(mock_run: Mock) -> None:
    mock_run.return_value = """
  pool: first_ok_zpool
 state: ONLINE
  scan: scrub in progress since Thu Aug 17 10:25:48 2017
    9,12T scanned out of 9,48T at 1,90M/s, 55h33m to go
    0 repaired, 96,19% done
config:

	NAME                                 STATE     READ WRITE CKSUM
	data                                 ONLINE       0     0     0
	  raidz1-0                           ONLINE       0     0     0
	    ata-ST3000DM001-1CH166_Z1F324L3  ONLINE       0     0     0

errors: No known data errors'
"""
    status = PoolStatus("first_ok_zpool")
    assert status.progress == 96.19
    assert status.speed == 1.9
    assert status.since == datetime(2017, 8, 17, 10, 25, 48)
