from tests.helper import execute_main as main

# setup() {
# 	. ./test/lib/test-helper.sh
# 	mock_path test/bin
# 	source_exec check_zpool_scrub
# }

# ##
# # Info options
# ##

# @test "run ./check_zpool_scrub -h" {
# 	run ./check_zpool_scrub -h
# 	[ "$status" -eq 0 ]
# 	[ "${lines[0]}" = "check_zpool_scrub v$VERSION" ]
# }

# @test "run ./check_zpool_scrub --help" {
# 	run ./check_zpool_scrub --help
# 	[ "$status" -eq 0 ]
# 	[ "${lines[0]}" = "check_zpool_scrub v$VERSION" ]
# }

# @test "run ./check_zpool_scrub -s" {
# 	run ./check_zpool_scrub -s
# 	[ "$status" -eq 0 ]
# 	[ "${lines[0]}" = "Monitoring plugin to check how long ago the \
# last ZFS scrub was performed." ]
# }

# @test "run ./check_zpool_scrub --short-description" {
# 	run ./check_zpool_scrub --short-description
# 	[ "$status" -eq 0 ]
# 	[ "${lines[0]}" = "Monitoring plugin to check how long ago the \
# last ZFS scrub was performed." ]
# }

# # Order;
# # critical
# # to
# # now

# ##
# # Return status
# ##

# @test "run ./check_zpool_^scrub -p first_critical_zpool" {
# 	run ./check_zpool_scrub -p first_critical_zpool
# 	[ "$status" -eq 2 ]
# }


def test_first_critical_zpool() -> None:
    result = main(["-p", "first_critical_zpool"])
    assert result.exitcode == 2
    assert result.stdout
    assert (
        "ZPOOL_SCRUB CRITICAL - first_critical_zpool_last_scrub is 0 (outside range @0:5356800) | first_critical_zpool_last_scrub=0;@2678400;@5356800"
        == result.first_line
    )


# @test "run ./check_zpool_scrub -p last_warning_zpool" {
# 	run ./check_zpool_scrub -p last_warning_zpool
# 	[ "$status" -eq 1 ]
# }

# @test "run ./check_zpool_scrub -p last_ok_zpool" {
# 	run ./check_zpool_scrub -p last_ok_zpool
# 	[ "$status" -eq 0 ]
# }

# @test "run ./check_zpool_scrub -p first_ok_zpool" {
# 	run ./check_zpool_scrub -p first_ok_zpool
# 	[ "$status" -eq 0 ]
# }

# ##
# # Warning / critical options
# ##

# @test "run ./check_zpool_scrub -p first_ok_zpool -w 1 -c 2" {
# 	run ./check_zpool_scrub -p first_ok_zpool -w 1 -c 2
# 	[ "$status" -eq 0 ]
# }

# @test "run ./check_zpool_scrub -p first_ok_zpool -w 2 -c 1" {
# 	run ./check_zpool_scrub -p first_ok_zpool -w 2 -c 1
# 	[ "$status" -eq 3 ]
# 	[ "${lines[0]}" = "<warntime> must be smaller than \
# <crittime>." ]
# }

# @test "run ./check_zpool_scrub --pool=first_ok_zpool --warning=2 --critical=1" {
# 	run ./check_zpool_scrub --pool=first_ok_zpool --warning=2 \
# 		--critical=1
# 	[ "$status" -eq 3 ]
# 	[ "${lines[0]}" = "<warntime> must be smaller than \
# <crittime>." ]
# }

# ##
# # Errors
# ##

# @test "run ./check_zpool_scrub -p unknown_zpool" {
# 	run ./check_zpool_scrub -p unknown_zpool
# 	[ "$status" -eq 3 ]
# 	[ "${lines[0]}" = "UNKNOWN: 'unknown_zpool' is no ZFS pool." ]
# }

# @test "run ./check_zpool_scrub --pool=unknown_zpool" {
# 	run ./check_zpool_scrub --pool=unknown_zpool
# 	[ "$status" -eq 3 ]
# 	[ "${lines[0]}" = "UNKNOWN: 'unknown_zpool' is no ZFS pool." ]
# }

# @test "run ./check_zpool_scrub --lol" {
# 	run ./check_zpool_scrub --lol
# 	[ "$status" -eq 2 ]
# 	[ "${lines[0]}" = "Invalid option “--lol”!" ]
# }

# ##
# # Output
# ##

# @test "run ./check_zpool_scrub -p first_critical_zpool OUTPUT" {
# 	run ./check_zpool_scrub -p first_critical_zpool
# 	[ "$status" -eq 2 ]
# 	local TEST="CRITICAL: The last scrub on zpool \
# 'first_critical_zpool' was performed on 2017-06-16.10:25:47. \
# | \
# first_critical_zpool_last_ago=5356801s;2678400;5356800;0 \
# first_critical_zpool_progress=100%;;;0;100 \
# first_critical_zpool_speed=0 \
# first_critical_zpool_time=0s"
# 	[ "${lines[0]}" = "$TEST" ]
# }

# @test "run ./check_zpool_scrub -p first_warning_zpool OUTPUT" {
# 	run ./check_zpool_scrub -p first_warning_zpool
# 	[ "$status" -eq 1 ]
# 	local TEST="WARNING: The last scrub on zpool \
# 'first_warning_zpool' was performed on 2017-07-17.10:25:47. \
# | \
# first_warning_zpool_last_ago=2678401s;2678400;5356800;0 \
# first_warning_zpool_progress=72.38%;;;0;100 \
# first_warning_zpool_speed=57.4 \
# first_warning_zpool_time=51120s"
# 	[ "${lines[0]}" = "$TEST" ]
# }

# @test "run ./check_zpool_scrub -p first_ok_zpool OUTPUT" {
# 	run ./check_zpool_scrub -p first_ok_zpool
# 	[ "$status" -eq 0 ]
# 	local TEST="OK: The last scrub on zpool 'first_ok_zpool' \
# was performed on 2017-08-17.10:25:48. \
# | \
# first_ok_zpool_last_ago=0s;2678400;5356800;0 \
# first_ok_zpool_progress=96.19%;;;0;100 \
# first_ok_zpool_speed=1.90 \
# first_ok_zpool_time=199980s"
# 	[ "${lines[0]}" = "$TEST" ]
# }

# @test "run ./check_zpool_scrub -p never_scrubbed_zpool OUTPUT" {
# 	run ./check_zpool_scrub -p never_scrubbed_zpool
# 	[ "$status" -eq 3 ]
# 	local TEST="UNKNOWN: The pool 'never_scrubbed_zpool' has never had a scrub."
# 	[ "${lines[0]}" = "$TEST" ]
# }

# @test "run ./check_zpool_scrub (all pools)" {
# 	run ./check_zpool_scrub
# 	[ "$status" -eq 2 ]
# 	TEST="UNKNOWN: 'unknown_zpool' is no ZFS pool. \
# UNKNOWN: The pool 'never_scrubbed_zpool' has never had a scrub. \
# OK: The last scrub on zpool 'first_ok_zpool' was performed on 2017-08-17.10:25:48. \
# OK: The last scrub on zpool 'last_ok_zpool' was performed on 2017-07-17.10:25:48. \
# WARNING: The last scrub on zpool 'first_warning_zpool' was performed on 2017-07-17.10:25:47. \
# WARNING: The last scrub on zpool 'last_warning_zpool' was performed on 2017-06-16.10:25:48. \
# CRITICAL: The last scrub on zpool 'first_critical_zpool' was performed on 2017-06-16.10:25:47. \
# | \
# first_ok_zpool_last_ago=0s;2678400;5356800;0 first_ok_zpool_progress=96.19%;;;0;100 first_ok_zpool_speed=1.90 first_ok_zpool_time=199980s \
# last_ok_zpool_last_ago=2678400s;2678400;5356800;0 last_ok_zpool_progress=96.19%;;;0;100 last_ok_zpool_speed=1.90 last_ok_zpool_time=199980s \
# first_warning_zpool_last_ago=2678401s;2678400;5356800;0 first_warning_zpool_progress=72.38%;;;0;100 first_warning_zpool_speed=57.4 first_warning_zpool_time=51120s \
# last_warning_zpool_last_ago=5356800s;2678400;5356800;0 last_warning_zpool_progress=72.38%;;;0;100 last_warning_zpool_speed=57.4 last_warning_zpool_time=51120s \
# first_critical_zpool_last_ago=5356801s;2678400;5356800;0 first_critical_zpool_progress=100%;;;0;100 first_critical_zpool_speed=0 first_critical_zpool_time=0s"
# 	[ "${lines[0]}" = "$TEST" ]
# }
