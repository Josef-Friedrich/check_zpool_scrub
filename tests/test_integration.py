from tests.helper import execute_main as main


def test_first_ok_zpool() -> None:
    result = main(["-p", "first_ok_zpool"])
    assert result.exitcode == 0
    assert result.stdout
    assert (
        "ZPOOL_SCRUB OK | 'first_ok_zpool: last_scrub_timespan'=0s 'first_ok_zpool: last_scrub_timestamp'=1502965548 'first_ok_zpool: progress'=96.19% 'first_ok_zpool: speed'=1.9m/s 'first_ok_zpool: time_to_go'=199980s"
        == result.first_line
    )


def test_last_ok_zpool() -> None:
    result = main(["-p", "last_ok_zpool"])
    assert result.exitcode == 0
    assert result.stdout
    assert (
        "ZPOOL_SCRUB OK | 'last_ok_zpool: last_scrub_timespan'=2678400s 'last_ok_zpool: last_scrub_timestamp'=1500287148 'last_ok_zpool: progress'=96.19% 'last_ok_zpool: speed'=1.9m/s 'last_ok_zpool: time_to_go'=199980s"
        == result.first_line
    )


def test_first_warning_zpool() -> None:
    result = main(["-p", "first_warning_zpool"])
    assert result.exitcode == 1
    assert result.stdout
    assert (
        "ZPOOL_SCRUB WARNING - Pool “first_warning_zpool”: 2678401 >= 5356800 | 'first_warning_zpool: last_scrub_timespan'=2678401s 'first_warning_zpool: last_scrub_timestamp'=1500287147 'first_warning_zpool: progress'=72.38% 'first_warning_zpool: speed'=57.4m/s 'first_warning_zpool: time_to_go'=51120s"
        == result.first_line
    )


def test_last_warning_zpool() -> None:
    result = main(["-p", "last_warning_zpool"])
    assert result.exitcode == 1
    assert result.stdout
    assert (
        "ZPOOL_SCRUB WARNING - Pool “last_warning_zpool”: 5356800 >= 5356800 | 'last_warning_zpool: last_scrub_timespan'=5356800s 'last_warning_zpool: last_scrub_timestamp'=1497608748 'last_warning_zpool: progress'=72.38% 'last_warning_zpool: speed'=57.4m/s 'last_warning_zpool: time_to_go'=51120s"
        == result.first_line
    )


def test_first_critical_zpool() -> None:
    result = main(["-p", "first_critical_zpool"])
    assert result.exitcode == 2
    assert result.stdout
    assert (
        "ZPOOL_SCRUB CRITICAL - Pool “first_critical_zpool”: 5356801 >= 5356800 | 'first_critical_zpool: last_scrub_timespan'=5356801s 'first_critical_zpool: last_scrub_timestamp'=1497608747"
        == result.first_line
    )


def test_all_pools() -> None:
    result = main([])
    assert result.exitcode == 3
    assert result.stdout
    assert (
        "ZPOOL_SCRUB UNKNOWN - The pool “unknown_zpool” has never had a scrub. | 'first_critical_zpool: last_scrub_timespan'=5356801s 'first_critical_zpool: last_scrub_timestamp'=1497608747 'first_ok_zpool: last_scrub_timespan'=0s 'first_ok_zpool: last_scrub_timestamp'=1502965548 'first_ok_zpool: progress'=96.19% 'first_ok_zpool: speed'=1.9m/s 'first_ok_zpool: time_to_go'=199980s 'first_warning_zpool: last_scrub_timespan'=2678401s 'first_warning_zpool: last_scrub_timestamp'=1500287147 'first_warning_zpool: progress'=72.38% 'first_warning_zpool: speed'=57.4m/s 'first_warning_zpool: time_to_go'=51120s 'last_ok_zpool: last_scrub_timespan'=2678400s 'last_ok_zpool: last_scrub_timestamp'=1500287148 'last_ok_zpool: progress'=96.19% 'last_ok_zpool: speed'=1.9m/s 'last_ok_zpool: time_to_go'=199980s 'last_warning_zpool: last_scrub_timespan'=5356800s 'last_warning_zpool: last_scrub_timestamp'=1497608748 'last_warning_zpool: progress'=72.38% 'last_warning_zpool: speed'=57.4m/s 'last_warning_zpool: time_to_go'=51120s"
        == result.first_line
    )


def test_warning() -> None:
    result = main(["-p", "first_ok_zpool", "-w", "1", "-c", "2"])
    assert result.exitcode == 0
    assert result.stdout
    assert (
        "ZPOOL_SCRUB OK | 'first_ok_zpool: last_scrub_timespan'=0s 'first_ok_zpool: last_scrub_timestamp'=1502965548 'first_ok_zpool: progress'=96.19% 'first_ok_zpool: speed'=1.9m/s 'first_ok_zpool: time_to_go'=199980s"
        == result.first_line
    )


def test_warning_gt_critical() -> None:
    result = main(["--warning", "2", "--critical", "1"])
    assert result.exitcode == 3
    assert result.stdout
    assert (
        "ZPOOL_SCRUB UNKNOWN: ValueError: -w SECONDS must be smaller than -c SECONDS. -w 2.0 > -c 1.0"
        == result.first_line
    )


def test_unknown_option() -> None:
    result = main(["--lol"])
    assert result.exitcode == 3
    assert result.stdout
    assert (
        "usage: check_zpool_scrub [-h] [-V] [-v] [-p POOL] [-w WARNING] [-c CRITICAL]"
        == result.first_line
    )
