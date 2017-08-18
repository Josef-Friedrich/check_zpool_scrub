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
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p last_warning_zpool" {
	run ./check_zpool_scrub -p last_warning_zpool
	[ "$status" -eq 1 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p first_warning_zpool" {
	run ./check_zpool_scrub -p first_warning_zpool
	[ "$status" -eq 1 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p last_ok_zpool" {
	run ./check_zpool_scrub -p last_ok_zpool
	[ "$status" -eq 0 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p first_ok_zpool" {
	run ./check_zpool_scrub -p first_ok_zpool
	[ "$status" -eq 0 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}
