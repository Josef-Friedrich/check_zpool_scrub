#!/usr/bin/env bats

setup() {
	. ./test/lib/test-helper.sh
	mock_path test/bin
	source_exec check_zpool_scrub
}

@test "function _last_scrub_date" {
	_last_scrub_date data
	result=$(_last_scrub_date data)
	echo $result > $HOME/debugg
}
