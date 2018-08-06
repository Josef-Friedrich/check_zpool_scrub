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

@test "function _datetime_to_timestamp" {
	result=$(_datetime_to_timestamp 2017-07-17.10:25:48)
	[ "$result" -eq 1500279948 ]
}

##
# progress
##

@test "function _progress_normalize" {
	[ "$(_progress_normalize 96,19%)" = '96.19' ]
	[ "$(_progress_normalize 72,38%)" = '72.38' ]
	[ -z "$(_progress_normalize)" ]
}

##
# speed
##

@test "function _speed_normalize" {
	[ "$(_speed_normalize 1,90M/s)" = '1.90' ]
	[ "$(_speed_normalize 111,90M/s)" = '111.90' ]
	[ "$(_speed_normalize 872,90K/s)" = '0.852441' ]
	[ "$(_speed_normalize 12K/s)" = '0.0117188' ]
}

##
# time to go
##

@test "function _time_to_min" {
	[ "$(_time_to_min 1h1m)" -eq 61 ]
	[ "$(_time_to_min 1h0m)" -eq 60 ]
	[ "$(_time_to_min 11h11m)" -eq 671 ]
}
