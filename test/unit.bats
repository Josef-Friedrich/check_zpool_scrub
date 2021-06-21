#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

##
# last scrub timestamp
##

@test "function _grab_last_scrub_timestamp" {
	[ "$(_grab_last_scrub_timestamp first_ok_zpool)" -eq 1502958348 ]
	[ "$(_grab_last_scrub_timestamp first_warning_zpool)" -eq 1500279947 ]
	[ "$(_grab_last_scrub_timestamp first_critical_zpool)" -eq 1497601547 ]
}

##
# progress
##

@test "function _grab_progress" {
	[ "$(_grab_progress first_ok_zpool)" = '96.19' ]
	[ "$(_grab_progress first_warning_zpool)" = '72.38' ]
	[ "$(_grab_progress first_critical_zpool)" -eq 100 ]
	[ "$(_grab_progress days_to_go)" = '52.05' ]
}

##
# speed
##

@test "function _grab_speed" {
	[ "$(_grab_speed first_ok_zpool)" = '1.90' ]
	[ "$(_grab_speed first_warning_zpool)" = '57.4' ]
	[ "$(_grab_speed first_critical_zpool)" -eq 0 ]
	[ "$(_grab_speed days_to_go)" -eq 120 ]
}

##
# time to go
##

@test "function _grab_time_to_go" {
	[ "$(_grab_time_to_go first_ok_zpool)" -eq 199980 ]
	[ "$(_grab_time_to_go first_warning_zpool)" -eq 51120 ]
	[ "$(_grab_time_to_go first_critical_zpool)" -eq 0 ]
	[ "$(_grab_time_to_go days_to_go)" -eq 3681 ]
	[ "$(_grab_time_to_go time_to_go_colons)" -eq 3681 ]
}

##
# main
##

@test "function _check_one_pool first_ok_zpool" {
	_check_one_pool first_ok_zpool
	[ "$STATE" -eq 0 ]
	[ "$MESSAGE" = "OK: The last scrub on zpool 'first_ok_zpool' \
was performed on 2017-08-17.10:25:48." ]
	[ "$PERFORMANCE_DATA" = "first_ok_zpool_last_ago=0;2678400;5356800 \
first_ok_zpool_progress=96.19 first_ok_zpool_speed=1.90 \
first_ok_zpool_time=199980" ]
}

@test "function _check_one_pool days_to_go" {
	_check_one_pool days_to_go
	[ "$STATE" -eq 0 ]
	[ "$MESSAGE" = "OK: The last scrub on zpool 'days_to_go' \
was performed on 2017-08-17.10:25:48." ]
	[ "$PERFORMANCE_DATA" = "days_to_go_last_ago=0;2678400;5356800 \
days_to_go_progress=52.05 days_to_go_speed=120 \
days_to_go_time=3681" ]
}

@test "function _check_multiple_pools first_ok_zpool" {
	_check_multiple_pools first_ok_zpool
	[ "$STATE" -eq 0 ]
	[ "$MESSAGE" = "OK: The last scrub on zpool 'first_ok_zpool' \
was performed on 2017-08-17.10:25:48." ]
	[ "$PERFORMANCE_DATA" = "first_ok_zpool_last_ago=0;2678400;5356800 \
first_ok_zpool_progress=96.19 first_ok_zpool_speed=1.90 \
first_ok_zpool_time=199980" ]
}


@test "function _check_multiple_pools first_ok_zpool last_ok_zpool" {
	_check_multiple_pools first_ok_zpool last_ok_zpool
	[ "$STATE" -eq 0 ]

	TEST="OK: The last scrub on zpool 'first_ok_zpool' was \
performed on 2017-08-17.10:25:48. \
OK: The last scrub on zpool 'last_ok_zpool' was performed on \
2017-07-17.10:25:48."
	[ "$MESSAGE" = "$TEST" ]

	TEST="first_ok_zpool_last_ago=0;2678400;5356800 \
first_ok_zpool_progress=96.19 \
first_ok_zpool_speed=1.90 \
first_ok_zpool_time=199980 \
last_ok_zpool_last_ago=2678400;2678400;5356800 \
last_ok_zpool_progress=96.19 \
last_ok_zpool_speed=1.90 \
last_ok_zpool_time=199980"
	[ "$PERFORMANCE_DATA" = "$TEST" ]
}

# warning

@test "function _check_multiple_pools first_ok first_warning" {
	_check_multiple_pools \
		first_ok_zpool \
		first_warning_zpool
	[ "$STATE" -eq 1 ]
}

@test "function _check_multiple_pools first_warning first_ok" {
	_check_multiple_pools \
		first_warning_zpool \
		first_ok_zpool
	[ "$STATE" -eq 1 ]
}

@test "function _check_multiple_pools first_warning first_ok never_scrubbed" {
	_check_multiple_pools \
		first_warning_zpool \
		first_ok_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 1 ]
}

# critical

@test "function _check_multiple_pools first_ok first_critical" {
	_check_multiple_pools \
		first_ok_zpool \
		first_critical_zpool
	[ "$STATE" -eq 2 ]
}

@test "function _check_multiple_pools first_critical first_ok" {
	_check_multiple_pools \
		first_critical_zpool \
		first_ok_zpool
	[ "$STATE" -eq 2 ]
}

@test "function _check_multiple_pools first_critical first_ok first_warning never_scrubbed" {
	_check_multiple_pools \
		first_critical_zpool \
		first_ok_zpool \
		first_warning_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 2 ]
}

# unknown

@test "function _check_multiple_pools first_ok never_scrubbed" {
	_check_multiple_pools \
		first_ok_zpool \
		never_scrubbed_zpool
	[ "$STATE" -eq 3 ]
}

@test "function _check_multiple_pools never_scrubbed first_ok" {
	_check_multiple_pools \
		never_scrubbed_zpool \
		first_ok_zpool
	[ "$STATE" -eq 3 ]
}
