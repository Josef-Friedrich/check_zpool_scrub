#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

##
# last scrub
##

@test "function _last_scrub_history_grab_datetime_from_command" {
	result=$(_last_scrub_history_grab_datetime_from_command last_ok_zpool)
	[ "$result" = '2017-07-17.10:25:48' ]
}

@test "function _last_scrub_history_to_timestamp" {
	[ "$(_last_scrub_history_to_timestamp first_critical_zpool)" -eq 1497601547 ]
	[ "$(_last_scrub_history_to_timestamp last_ok_zpool)" -eq 1500279948 ]
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
	[ "$(_time_grep unkown_zpool)" = '' ]
	[ "$(_time_grep first_ok_zpool)" = '55h33m' ]
	[ "$(_time_grep first_warning_zpool)" = '14h12m' ]
	[ "$(_time_grep first_critical_zpool)" = '' ]

}

@test "function _time" {
	[ "$(_time first_ok_zpool)" -eq 3333 ]
	[ "$(_time first_warning_zpool)" -eq 852 ]
	[ "$(_time first_critical_zpool)" -eq 0 ]
}
