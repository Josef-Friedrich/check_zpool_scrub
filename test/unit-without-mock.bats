#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	source_exec check_zpool_scrub
}

##
# date
##

@test "function _now_to_year" {
	result=$(_now_to_year)
	[ "$result" -eq "$(date +%Y)" ]
}

@test "function _date_to_year" {
	result=$(_date_to_year 2016-09-08)
	[ "$result" -eq 2016 ]
}

@test "function _timestamp_to_datetime" {
	result=$(_timestamp_to_datetime 1497601547)
	[ "$result" = "2017-06-16.10:25:47" ]
}

@test "function _now_to_timestamp" {
	result=$(_now_to_timestamp)
	[ "$result" -gt 1533570437 ]
}

@test "function _ctime_to_timestamp" {
	result=$(_ctime_to_timestamp 'Mon Jul 17 10:25:48 2017')
	[ "$result" -eq 1500279948 ]
}

@test "function _performance_data_one_pool" {
	result="$(_performance_data_one_pool pool 1 2 3 4)"
	[ "$result" = "pool_last_ago=1 pool_progress=2 pool_speed=3 \
pool_time=4" ]
}
