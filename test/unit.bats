#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

@test "function _last_scrub_date" {
	result=$(_last_scrub_date last_ok_zpool)
	[ "$result" = '2017-07-17.10:25:48' ]
}

@test "function _date_to_timestamp" {
	result=$(_date_to_timestamp 2017-07-17.10:25:48)
	[ "$result" -eq 1500279948 ]
}

@test "function _get_last_scrub" {
	result=$(_get_last_scrub last_ok_zpool)
	[ "$result" -eq 1500279948 ]
}

@test "function _scrub_progress" {
	result=$(_scrub_progress first_ok_zpool)
	[ "$result" = '96.19' ]
}

@test "function _scrub_speed" {
	result=$(_scrub_speed first_ok_zpool)
	[ "$result" = '1,90M/s' ]
}

@test "function _scrub_speed_normalize" {
	[ "$(_scrub_speed_normalize 1,90M/s)" = '1.90' ]
	[ "$(_scrub_speed_normalize 111,90M/s)" = '111.90' ]
	[ "$(_scrub_speed_normalize 872,90K/s)" = '0.852441' ]
	[ "$(_scrub_speed_normalize 12K/s)" = '0.0117188' ]
}

@test "function _grep_time_to_go" {
	[ "$(_grep_time_to_go first_ok_zpool)" = '55h33m' ]
	[ "$(_grep_time_to_go first_warning_zpool)" = '14h12m' ]
}

@test "function _time_to_min" {
	[ "$(_time_to_min 1h1m)" = '61' ]
	[ "$(_time_to_min 1h0m)" = '60' ]
	[ "$(_time_to_min 11h11m)" = '671' ]
}

@test "function _time_to_go" {
	[ "$(_time_to_go first_ok_zpool)" -eq 3333 ]
	[ "$(_time_to_go first_warning_zpool)" -eq 852 ]
	[ "$(_time_to_go finished_scrub)" -eq 0 ]
}
