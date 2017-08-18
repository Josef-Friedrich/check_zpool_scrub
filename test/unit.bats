#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

@test "function _last_scrub_date" {
	result=$(_last_scrub_date ok_zpool)
	[ "$result" = '2017-07-17.10:25:48' ]
}

@test "function _date_to_timestamp" {
	result=$(_date_to_timestamp 2017-07-17.10:25:48)
	[ "$result" -eq 1500279948 ]
}

@test "function _get_last_scrub" {
	result=$(_get_last_scrub ok_zpool)
	[ "$result" -eq 1500279948 ]
}
