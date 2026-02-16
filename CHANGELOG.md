# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Add subprocess
- Add boilerplate files
- Add more boilerplate files
- Add rewrite notice
- Add description and epilog to the argparser
- Add dependency
- Add some boilerplate files to start a rewrite in Python

### Changed
- Parse ctime
- Test on >=3.10
- Implement progress and since
- Migrate from poetry to uv
- Merge branch 'main' of github.com:Josef-Friedrich/check_zpool_scrub
- Update dependencies
- Update tooling
- Fix all tests
- Merge branch 'master' of github.com:Josef-Friedrich/check_zpool_scrub
- Upgrade nagiosplugin-stubs to v0.4.0
- Implement --version
- Configure the argparser
- Fix broken arithmetic expression for calculating the time to go #15


## [2.0] - 2021-06-23

### Changed
- Bump version 2.0
- Merge pull request #14 from taam/master in [#14](https://github.com/Josef-Friedrich/check_zpool_scrub/pull/14)
- Performance data with units
- Time to go in seconds (instead of minutes)
- Fix the performance data format of *_last_ago values #13


## [1.7] - 2021-06-03

### Added
- Add some docs
- Add new time to go function

### Changed
- Bump version 1.7
- Make function _grab_time_to_go more robust #11
- Reduce calls of `zpool status` #12
- Merge three function into one
- Fix inconsistent indentation #12
- Fix #11
- Test speed function
- Test new function to grab time to go
- Fix zpool status should not be called multiple times (per pool) #12
- Clean up
- Update copyright


## [1.6] - 2019-08-13

### Changed
- Update version in the README
- Bump version 1.6
- Fix #11 check_zpool_scrub: Illegal number


## [1.5] - 2019-07-10

### Changed
- Bump version 1.5
- Show the pool name in a UNKOWN message for a pool that has never been scrubed


## [1.4] - 2019-07-09

### Changed
- Bump version 1.4
- Merge pull request #9 from SlothOfAnarchy/patch-1 in [#9](https://github.com/Josef-Friedrich/check_zpool_scrub/pull/9)
- Move OS evaluation to the top, before its first usage


## [1.3] - 2018-08-22

### Added
- Add unit tests for _check_multiple_pools
- Add unittest for _check* functions
- Add unit test for _performance_data_one_pool
- Add code to support multiple pools
- Add more line breaks for better readability
- Add some comments
- Add some date functions
- Add some comments
- Add integration test for sudo
- Add tests for the options “-r” and “--sudo”
- Add sudoers.d file to go with the --sudo flag
- Add --sudo flag to enable sudo use (Fixes outstanding testsuite failures)

### Changed
- Bump version 1.3
- Refactor tests
- Extend cli docs
- Rearrange code
- Fix punctation
- Short lines for better readability
- Replace Solaris with Darwin in icingaexchange.yml
- Test all pools
- Shorter lines for better readability
- Unify punctation
- Delete empty line
- Handle unknown state never scrubbed
- Handle unknown zpools
- Get rid of some variables
- Calculate GLOBAL_STATE for all pools
- Do not print cricital and warning performance data values for each pool
- Prepare for string concatenation
- Use global variables to split output of functions
- Document more global variables
- Section for global variables
- Rename variable to fit better to the STATE_ variables
- Pool should be first positional argument
- Prefix performance data labels with pool name
- Prepare for #4
- Fix date error #6
- Merge pull request #8 from dlangille/patch-2 in [#8](https://github.com/Josef-Friedrich/check_zpool_scrub/pull/8)
- Change _usage to echo "$USAGE"
- Fix progress is incorrect #7
- Fix tests
- Merge pull request #5 from dlangille/patch-1 in [#5](https://github.com/Josef-Friedrich/check_zpool_scrub/pull/5)
- When critical, the pool name is slightly obscured
- Get rid of --sudo
- Set timezone on Travis CI to fix tests
- Use only zpool status to get last scrub date
- Use new function _get_last_scrub_timestamp
- Rewrite last scrub functions
- Grab ctime from zpool status
- Delete duplicate code
- Test some more code without mocking any commands
- Test without mocking the date command
- Convert ctime to UNIX timestamp
- Extract status strings from zfs c code
- Adjust date mock for FreeBSD
- Rewrite date functions
- Mock date for FreeBSD
- Fix whitespace in description
- Fix date: illegal time format #3
- Does not work on FreeBSD #2
- Play around with awk
- Speed up `zpool history` #3
- Create description
- Update README
- Update boilerplate files
- Update project url
- Simplify the handling of the command “sudo”
- Coding style: Use uppercase variable names
- Readd accidentially delete skeleton.sh
- Sync skeleton
- Update README.md
- Merge pull request #1 from valgrind/master in [#1](https://github.com/Josef-Friedrich/check_zpool_scrub/pull/1)
- Handle edge cases: Unscrubbed disk and script not running as root
- Fix indentation

### Removed
- Remove debug line


## [1.1] - 2017-09-07

### Added
- Add output tests
- Add more tests
- Add speed to performance data
- Add new performance data
- Add more c code
- Add c code for examination
- Add new functions
- Add performanced data
- Add project pages
- Add more variables
- Add icingaexchange.yml
- Add more tests
- Add new functions
- Add calculations for tests
- Add some tests
- Add mock binaries
- Add binaries
- Add first test

### Changed
- Version 1.1
- Sync skeleton
- Test options
- Sync with skeleton
- Sync with skeleton
- Sync with skeleton
- Rename test file
- Refactor progress
- Fix variable name
- Refactor performance data time
- Refactor performance data speed
- Implement new performance data: time_to_go
- Better speed calculation
- Fix obsolete _usage function
- Update icinga.yml
- Update README
- Fix tests
- Improve documentation
- Fix url
- Update short description
- Update README
- Implement long options
- Test more datasets
- Delete prefix
- Reformat license
- Sync with skeleton
- Create README.md

### Removed
- Remove debug code


[unreleased]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/2.0..HEAD
[2.0]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.7..2.0
[1.7]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.6..1.7
[1.6]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.5..1.6
[1.5]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.4..1.5
[1.4]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.3..1.4
[1.3]: https://github.com/Josef-Friedrich/check_zpool_scrub/compare/1.1..1.3

<!-- generated by git-cliff -->
