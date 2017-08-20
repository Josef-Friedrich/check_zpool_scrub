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

##
# progress
##

@test "function _progress_grep" {
	[ "$(_progress_grep first_ok_zpool)" = '96,19%' ]
	[ "$(_progress_grep first_warning_zpool)" = '72,38%' ]
	[ -z "$(_progress_grep finished_scrub)" ]
}

@test "function _progress_normalize" {
	[ "$(_progress_normalize 96,19%)" = '96.19' ]
	[ "$(_progress_normalize 72,38%)" = '72.38' ]
	[ -z "$(_progress_normalize)" ]
}

@test "function _progress" {
	[ "$(_progress first_ok_zpool)" = '96.19' ]
	[ "$(_progress first_warning_zpool)" = '72.38' ]
	[ "$(_progress finished_scrub)" -eq 100 ]
}

##
# speed
##

@test "function _speed_grep" {
	[ "$(_speed_grep first_ok_zpool)" = '1,90M/s' ]
}

@test "function _speed_normalize" {
	[ "$(_speed_normalize 1,90M/s)" = '1.90' ]
	[ "$(_speed_normalize 111,90M/s)" = '111.90' ]
	[ "$(_speed_normalize 872,90K/s)" = '0.852441' ]
	[ "$(_speed_normalize 12K/s)" = '0.0117188' ]
}

@test "function _speed" {
	[ "$(_speed first_ok_zpool)" = '1.90' ]
	[ "$(_speed first_warning_zpool)" = '57.4' ]
	[ "$(_speed finished_scrub)" -eq 0 ]
}

##
# time
##

@test "function _time_grep" {
	[ "$(_time_grep first_ok_zpool)" = '55h33m' ]
	[ "$(_time_grep first_warning_zpool)" = '14h12m' ]
}

@test "function _time_to_min" {
	[ "$(_time_to_min 1h1m)" = '61' ]
	[ "$(_time_to_min 1h0m)" = '60' ]
	[ "$(_time_to_min 11h11m)" = '671' ]
}

@test "function _time" {
	[ "$(_time first_ok_zpool)" -eq 3333 ]
	[ "$(_time first_warning_zpool)" -eq 852 ]
	[ "$(_time finished_scrub)" -eq 0 ]
}
