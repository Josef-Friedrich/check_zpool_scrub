#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

##
# Info options
##

@test "run ./check_zpool_scrub -h" {
	run ./check_zpool_scrub -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_zpool_scrub v$VERSION" ]
}

@test "run ./check_zpool_scrub --help" {
	run ./check_zpool_scrub --help
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = "check_zpool_scrub v$VERSION" ]
}

@test "run ./check_zpool_scrub -s" {
	run ./check_zpool_scrub -s
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = 'Monitoring plugin to check how long ago the last ZFS scrub was performed.' ]
}

@test "run ./check_zpool_scrub --short-description" {
	run ./check_zpool_scrub --short-description
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = 'Monitoring plugin to check how long ago the last ZFS scrub was performed.' ]
}

# Order;
# critical
# to
# now

##
# Return status
##

@test "run ./check_zpool_scrub -p first_critical_zpool" {
	run ./check_zpool_scrub -p first_critical_zpool
	[ "$status" -eq 2 ]
}

@test "run ./check_zpool_scrub -p last_warning_zpool" {
	run ./check_zpool_scrub -p last_warning_zpool
	[ "$status" -eq 1 ]
}

@test "run ./check_zpool_scrub -p last_ok_zpool" {
	run ./check_zpool_scrub -p last_ok_zpool
	[ "$status" -eq 0 ]
}

@test "run ./check_zpool_scrub -p first_ok_zpool" {
	run ./check_zpool_scrub -p first_ok_zpool
	[ "$status" -eq 0 ]
}

##
# Warning / critical options
##

@test "run ./check_zpool_scrub -p first_ok_zpool -w 1 -c 2" {
	run ./check_zpool_scrub -p first_ok_zpool -w 1 -c 2
	[ "$status" -eq 0 ]
}

@test "run ./check_zpool_scrub -p first_ok_zpool -w 2 -c 1" {
	run ./check_zpool_scrub -p first_ok_zpool -w 2 -c 1
	[ "$status" -eq 3 ]
	[ "${lines[0]}" = '<warntime> must be smaller than <crittime>' ]
}

@test "run ./check_zpool_scrub --pool=first_ok_zpool --warning=2 --critical=1" {
	run ./check_zpool_scrub --pool=first_ok_zpool --warning=2 --critical=1
	[ "$status" -eq 3 ]
	[ "${lines[0]}" = '<warntime> must be smaller than <crittime>' ]
}

##
# Errors
##

@test "run ./check_zpool_scrub -p unkown_zpool" {
	run ./check_zpool_scrub -p unkown_zpool
	[ "$status" -eq 3 ]
	[ "${lines[0]}" = '“unkown_zpool” is no ZFS pool!' ]
	[ "${lines[1]}" = "check_zpool_scrub v$VERSION" ]
}

@test "run ./check_zpool_scrub --pool=unkown_zpool" {
	run ./check_zpool_scrub --pool=unkown_zpool
	[ "$status" -eq 3 ]
	[ "${lines[0]}" = '“unkown_zpool” is no ZFS pool!' ]
}

@test "run ./check_zpool_scrub --lol" {
	run ./check_zpool_scrub --lol
	[ "$status" -eq 2 ]
	[ "${lines[0]}" = "Invalid option “--lol”!" ]
}

##
# Output
##

@test "run ./check_zpool_scrub -p first_critical_zpool OUTPUT" {
	run ./check_zpool_scrub -p first_critical_zpool
	[ "$status" -eq 2 ]
	local TEST="CRITICAL: The last scrub on zpool \
'first_critical_zpool' was performed on 2017-06-16.10:25:47 \
| first_critical_zpool_last_ago=5356801 first_critical_zpool_warning=2678400 first_critical_zpool_critical=5356800 first_critical_zpool_progress=100 \
first_critical_zpool_speed=0 first_critical_zpool_time=0"
	[ "${lines[0]}" = "$TEST" ]
}

@test "run ./check_zpool_scrub -p first_warning_zpool OUTPUT" {
	run ./check_zpool_scrub -p first_warning_zpool
	[ "$status" -eq 1 ]
	local TEST="WARNING: The last scrub on zpool \
'first_warning_zpool' was performed on 2017-07-17.10:25:47 \
| first_warning_zpool_last_ago=2678401 first_warning_zpool_warning=2678400 first_warning_zpool_critical=5356800 first_warning_zpool_progress=72.38 \
first_warning_zpool_speed=57.4 first_warning_zpool_time=852"
	[ "${lines[0]}" = "$TEST" ]
}

@test "run ./check_zpool_scrub -p first_ok_zpool OUTPUT" {
	run ./check_zpool_scrub -p first_ok_zpool
	[ "$status" -eq 0 ]
	local TEST="OK: The last scrub on zpool 'first_ok_zpool' \
was performed on 2017-08-17.10:25:48 \
| first_ok_zpool_last_ago=0 first_ok_zpool_warning=2678400 first_ok_zpool_critical=5356800 first_ok_zpool_progress=96.19 \
first_ok_zpool_speed=1.90 first_ok_zpool_time=3333"
	[ "${lines[0]}" = "$TEST" ]
}

@test "run ./check_zpool_scrub -p never_scrubbed_zpool OUTPUT" {
	run ./check_zpool_scrub -p never_scrubbed_zpool
	[ "$status" -eq 3 ]
	local TEST="UNKNOWN: The pool has never had a scrub."
	[ "${lines[0]}" = "$TEST" ]
}
