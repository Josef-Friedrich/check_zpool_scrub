import check_zpool_scrub
from tests.helper import run


class TestWithSubprocess:
    def test_help(self) -> None:
        process = run(["--help"])
        assert process.returncode == 0
        assert "usage: check_zpool_scrub" in process.stdout

    def test_version(self) -> None:
        process = run(
            ["--version"],
        )
        assert process.returncode == 0
        assert "check_zpool_scrub " + check_zpool_scrub.__version__ in process.stdout
