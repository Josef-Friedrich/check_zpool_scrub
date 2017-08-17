#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
}

@test "run ./check_zpool_scrub -h" {
	run ./check_zpool_scrub -h
	[ "$status" -eq 0 ]
	[ "${lines[0]}" = 'check_zfs_scrub' ]
}
