import re
import typing
from unittest.mock import Mock, patch

import pytest

from check_zpool_scrub import main
from tests.helper import execute_main


def side_effect(*args: typing.Any, **kwargs: typing.Any):
    if args[0] == ["zpool", "list", "-H", "-o", "name"]:
        return """unknown_zpool
never_scrubbed_zpool
first_ok_zpool
last_ok_zpool
first_warning_zpool
last_warning_zpool
first_critical_zpool"""


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


def test_help() -> None:
    result = execute_main(["--help"])

    assert result.exitcode == 3

    assert result.stdout
    assert "usage: check_zpool_scrub " in result.stdout
