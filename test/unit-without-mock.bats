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

##
# progress
##

@test "function _progress_normalize" {
	[ "$(_progress_normalize 96,19%)" = '96.19' ]
	[ "$(_progress_normalize 72,38%)" = '72.38' ]
	[ -z "$(_progress_normalize)" ]
}

##
# time to go
##

@test "function _last_scrub_grab_ctime_from_string: in process" {
	INPUT='  scan: scrub in progress since Sun Aug 13 00:24:02 2017'
	result="$(_last_scrub_grab_ctime_from_string "$INPUT")"
	[ "$result" = 'Sun Aug 13 00:24:02 2017' ]
}

@test "function _last_scrub_grab_ctime_from_string: finished" {
	INPUT="  scan: scrub repaired 0 in 266h29m with 0 errors on \
Tue Aug 15 01:12:31 2017"
	result="$(_last_scrub_grab_ctime_from_string "$INPUT")"
	[ "$result" = 'Tue Aug 15 01:12:31 2017' ]
}

@test "function _last_scrub_grab_ctime_from_string: multiple line" {
	INPUT="  pool: data
 state: ONLINE
  scan: scrub in progress since Sun Aug 13 00:24:02 2017
   7,34T scanned out of 10,1T at 57,4M/s, 14h12m to go
   0 repaired, 72,38% done"
	result="$(_last_scrub_grab_ctime_from_string "$INPUT")"
	[ "$result" = 'Sun Aug 13 00:24:02 2017' ]
}

@test "function _last_scrub_grab_ctime_from_string: canceled" {
	INPUT='  scan: scrub canceled on Tue Aug 15 01:12:31 2017'
	result="$(_last_scrub_grab_ctime_from_string "$INPUT")"
	[ "$result" = 'Tue Aug 15 01:12:31 2017' ]
}

@test "function _performance_data_one_pool" {
	result="$(_performance_data_one_pool pool 1 2 3 4)"
	[ "$result" = "pool_last_ago=1 pool_progress=2 pool_speed=3 \
pool_time=4" ]
}
