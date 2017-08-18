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

@test "run ./check_zpool_scrub -p ok_zpool" {
	run ./check_zpool_scrub -p ok_zpool
	[ "$status" -eq 0 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p warning_zpool" {
	run ./check_zpool_scrub -p warning_zpool
	[ "$status" -eq 1 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}

@test "run ./check_zpool_scrub -p critical_zpool" {
	run ./check_zpool_scrub -p critical_zpool
	[ "$status" -eq 2 ]
	#[ "${lines[0]}" = 'check_zfs_scrub' ]
}
