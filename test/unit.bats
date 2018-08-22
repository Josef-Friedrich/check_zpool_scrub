#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

##
# progress
##

@test "function _progress_grep" {
	[ "$(_progress_grep first_ok_zpool)" = '96,19%' ]
	[ "$(_progress_grep first_warning_zpool)" = '72,38%' ]
	[ -z "$(_progress_grep first_critical_zpool)" ]
}

@test "function _progress" {
	[ "$(_progress first_ok_zpool)" = '96.19' ]
	[ "$(_progress first_warning_zpool)" = '72.38' ]
	[ "$(_progress first_critical_zpool)" -eq 100 ]
}

##
# speed
##

@test "function _speed_grep" {
	[ "$(_speed_grep first_ok_zpool)" = '1,90M/s' ]
	[ "$(_speed_grep first_warning_zpool)" = '57,4M/s' ]
	[ -z "$(_speed_grep first_critical_zpool)" ]
}

@test "function _speed" {
	[ "$(_speed first_ok_zpool)" = '1.90' ]
	[ "$(_speed first_warning_zpool)" = '57.4' ]
	[ "$(_speed first_critical_zpool)" -eq 0 ]
}

##
# time to go
##

@test "function _time_grep" {
	[ "$(_time_grep unknown_zpool)" = '' ]
	[ "$(_time_grep first_ok_zpool)" = '55h33m' ]
	[ "$(_time_grep first_warning_zpool)" = '14h12m' ]
	[ "$(_time_grep first_critical_zpool)" = '' ]

}

@test "function _time" {
	[ "$(_time first_ok_zpool)" -eq 3333 ]
	[ "$(_time first_warning_zpool)" -eq 852 ]
	[ "$(_time first_critical_zpool)" -eq 0 ]
}

##
# main
##

@test "function _check_one_pool first_ok_zpool" {
	_check_one_pool first_ok_zpool
	[ "$STATE" -eq 0 ]
	[ "$MESSAGE" = "OK: The last scrub on zpool 'first_ok_zpool' was performed on 2017-08-17.10:25:48." ]
	[ "$PERFORMANCE_DATA" = 'first_ok_zpool_last_ago=0 first_ok_zpool_progress=96.19 first_ok_zpool_speed=1.90 first_ok_zpool_time=3333' ]
}

@test "function _check_multiple_pools first_ok_zpool" {
	_check_multiple_pools first_ok_zpool
	[ "$STATE" -eq 0 ]
	[ "$MESSAGE" = "OK: The last scrub on zpool 'first_ok_zpool' was performed on 2017-08-17.10:25:48." ]
	[ "$PERFORMANCE_DATA" = 'first_ok_zpool_last_ago=0 first_ok_zpool_progress=96.19 first_ok_zpool_speed=1.90 first_ok_zpool_time=3333' ]
}


@test "function _check_multiple_pools first_ok_zpool last_ok_zpool" {
	_check_multiple_pools first_ok_zpool last_ok_zpool
	[ "$STATE" -eq 0 ]

	TEST="OK: The last scrub on zpool 'first_ok_zpool' was \
performed on 2017-08-17.10:25:48. \
OK: The last scrub on zpool 'last_ok_zpool' was performed on \
2017-07-17.10:25:48."
	[ "$MESSAGE" = "$TEST" ]

	TEST="first_ok_zpool_last_ago=0 \
first_ok_zpool_progress=96.19 \
first_ok_zpool_speed=1.90 \
first_ok_zpool_time=3333 \
last_ok_zpool_last_ago=2678400 \
last_ok_zpool_progress=96.19 \
last_ok_zpool_speed=1.90 \
last_ok_zpool_time=3333"
	[ "$PERFORMANCE_DATA" = "$TEST" ]
}

# warning

@test "function _check_multiple_pools first_ok_zpool first_warning_zpool" {
	_check_multiple_pools \
		first_ok_zpool \
		first_warning_zpool
	[ "$STATE" -eq 1 ]
}

@test "function _check_multiple_pools first_warning_zpool first_ok_zpool" {
	_check_multiple_pools \
		first_warning_zpool \
		first_ok_zpool
	[ "$STATE" -eq 1 ]
}

@test "function _check_multiple_pools first_warning_zpool first_ok_zpool never_scrubbed_zpool" {
	_check_multiple_pools \
		first_warning_zpool \
		first_ok_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 1 ]
}

# critical

@test "function _check_multiple_pools first_ok_zpool first_critical_zpool" {
	_check_multiple_pools \
		first_ok_zpool \
		first_critical_zpool
	[ "$STATE" -eq 2 ]
}

@test "function _check_multiple_pools first_critical_zpool first_ok_zpool" {
	_check_multiple_pools \
		first_critical_zpool \
		first_ok_zpool
	[ "$STATE" -eq 2 ]
}

@test "function _check_multiple_pools first_critical_zpool first_ok_zpool first_warning_zpool never_scrubbed_zpool" {
	_check_multiple_pools \
		first_critical_zpool \
		first_ok_zpool \
		first_warning_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 2 ]
}

# unknown

@test "function _check_multiple_pools first_ok_zpool never_scrubbed_zpool" {
	_check_multiple_pools \
		first_ok_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 3 ]
}

@test "function _check_multiple_pools never_scrubbed_zpool first_ok_zpool" {
	_check_multiple_pools \
		never_scrubbed_zpool \
		first_ok_zpool
	[ "$STATE" -eq 3 ]
}
