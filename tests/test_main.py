import re
import typing
from importlib import metadata
from unittest.mock import Mock, patch

import pytest

from check_zpool_scrub import main
from tests.helper import execute_main

version: str = metadata.version("check_zpool_scrub")


def side_effect(*args: typing.Any, **kwargs: typing.Any):
    if args[0] == ["zpool", "list", "-H", "-o", "name"]:
        return """unknown_zpool
never_scrubbed_zpool
first_ok_zpool
last_ok_zpool
first_warning_zpool
last_warning_zpool
first_critical_zpool"""


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


@patch("check_zpool_scrub.subprocess.check_output")
def test_list_pools(check_output: Mock) -> None:
    check_output.side_effect = side_effect
    with pytest.raises(
        ValueError,
        match=re.escape(
            "-p xxx is not in ['unknown_zpool', 'never_scrubbed_zpool', 'first_ok_zpool', 'last_ok_zpool', 'first_warning_zpool', 'last_warning_zpool', 'first_critical_zpool']"
        ),
    ):
        main("--pool", "xxx")
