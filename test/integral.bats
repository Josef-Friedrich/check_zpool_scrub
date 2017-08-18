#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
}

@test "run ./check_zpool_scrub -h" {
	run ./check_zpool_scrub -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = 'check_zfs_scrub' ]
}

# Order;
# critical
# to
# now

@test "run ./check_zpool_scrub -p first_critical_zpool" {
	run ./check_zpool_scrub -p first_critical_zpool
	[ "$status" -eq 2 ]
}

@test "run ./check_zpool_scrub -p last_warning_zpool" {
	run ./check_zpool_scrub -p last_warning_zpool
	[ "$status" -eq 1 ]
}

@test "run ./check_zpool_scrub -p first_warning_zpool" {
	run ./check_zpool_scrub -p first_warning_zpool
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

@test "run ./check_zpool_scrub -p unkown_zpool" {
	run ./check_zpool_scrub -p unkown_zpool
	[ "$status" -eq 3 ]
	[ "${lines[0]}" = '“unkown_zpool” is no ZFS pool!' ]
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

@test "run ./check_zpool_scrub --short-description" {
	run ./check_zpool_scrub --short-description
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = 'Monitoring plugin to check how long ago the last ZFS scrub was performed.' ]
}
