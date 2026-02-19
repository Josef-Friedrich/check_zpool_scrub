from importlib import metadata

from tests.helper import execute_main

version: str = metadata.version("check_zpool_scrub")


def test_help_long() -> None:
    result = execute_main(["--help"])
    assert result.exitcode == 3
    assert result.stdout
    assert "usage: check_zpool_scrub " in result.stdout


def test_help_short() -> None:
    result = execute_main(["-h"])
    assert result.exitcode == 3
    assert result.stdout
    assert "usage: check_zpool_scrub " in result.stdout


def test_version_long() -> None:
    result = execute_main(["--version"])
    assert result.exitcode == 3
    assert result.stdout
    assert "check_zpool_scrub " + version in result.stdout


def test_version_short() -> None:
    result = execute_main(["-V"])
    assert result.exitcode == 3
    assert result.stdout
    assert "check_zpool_scrub " + version in result.stdout


def test_pool_long_unknown() -> None:
    result = execute_main(["--pool", "xxx"])
    assert result.exitcode == 3
    assert result.stdout
    assert (
        result.first_line
        == "ZPOOL_SCRUB UNKNOWN: ValueError: Unknown pool 'xxx'. Available pools: 'unknown_zpool', 'never_scrubbed_zpool', 'first_ok_zpool', 'last_ok_zpool', 'first_warning_zpool', 'last_warning_zpool', 'first_critical_zpool'"
    )
