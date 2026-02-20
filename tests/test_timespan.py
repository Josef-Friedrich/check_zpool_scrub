from check_zpool_scrub import _convert_timespan_to_sec  # type: ignore


class TestConvertTimespanToSec:
    """Tests for _convert_timespan_to_sec function."""

    def test_seconds(self) -> None:
        """Test conversion of seconds."""
        assert _convert_timespan_to_sec("5s") == 5
        assert _convert_timespan_to_sec("45.5s") == 46

    def test_minutes(self) -> None:
        """Test conversion of minutes."""
        assert _convert_timespan_to_sec("1m") == 60
        assert _convert_timespan_to_sec("2min") == 120
        assert _convert_timespan_to_sec("3minutes") == 180

    def test_hours(self) -> None:
        """Test conversion of hours."""
        assert _convert_timespan_to_sec("1h") == 3600
        assert _convert_timespan_to_sec("2hr") == 7200
        assert _convert_timespan_to_sec("3 hours") == 10800

    def test_days(self) -> None:
        """Test conversion of days."""
        assert _convert_timespan_to_sec("1d") == 86400
        assert _convert_timespan_to_sec("2days") == 172800

    def test_weeks(self) -> None:
        """Test conversion of weeks."""
        assert _convert_timespan_to_sec("1w") == 604800
        assert _convert_timespan_to_sec("2weeks") == 1209600

    def test_months(self) -> None:
        """Test conversion of months."""
        assert _convert_timespan_to_sec("1M") == 2630016
        assert _convert_timespan_to_sec("2months") == 5260032

    def test_years(self) -> None:
        """Test conversion of years."""
        assert _convert_timespan_to_sec("1y") == 31557600
        assert _convert_timespan_to_sec("2years") == 63115200

    def test_combined_timespan(self) -> None:
        """Test conversion of combined timespans."""
        assert _convert_timespan_to_sec("1h30m") == 5400
        assert _convert_timespan_to_sec("2 months 8 days") == 5951232
        assert _convert_timespan_to_sec("3min 45.234s") == 225

    def test_whitespace_handling(self) -> None:
        """Test that whitespace is properly handled."""
        assert _convert_timespan_to_sec("5 s") == 5
        assert _convert_timespan_to_sec("  10  minutes  ") == 600

    def test_decimal_values(self) -> None:
        """Test conversion with decimal values."""
        assert _convert_timespan_to_sec("1.5h") == 5400
        assert _convert_timespan_to_sec("2.5d") == 216000
