[![Build Status](https://travis-ci.org/Josef-Friedrich/check_zpool_scrub.svg?branch=master)](https://travis-ci.org/Josef-Friedrich/check_zpool_scrub)

# check_zpool_scrub


## Summary / Short description

> Monitoring plugin to check how long ago the last ZFS scrub was performed.

## Usage

```
check_zpool_scrub v1.7
Copyright (c) 2016-2021 Josef Friedrich <josef@friedrich.rocks>

Monitoring plugin to check how long ago the last ZFS scrub was performed.


Usage: check_zpool_scrub <options>

Options:
 -c, --critical=OPT_CRITICAL
    Interval in seconds for critical state.
 -p,--pool=OPT_POOL
    Name of the pool. If this option is omitted all pools are checked.
 -h, --help
    Show this help.
 -s, --short-description
    Show a short description / summary.
 -v, --version
    Show the version number.
 -w, --warning=OPT_WARNING
    Interval in seconds for warning state. Must be lower than -c.

Performance data:

POOL is the name of the pool

 - POOL_last_ago;warning;critical
    Time interval in seconds for last scrub.
 - POOL_progress
    Percent 0 - 100
 - POOL_speed
    MB per second.
 - POOL_time
    Time to go in minutes.

Details about the implementation of this monitoring plugin:

This monitoring plugin grabs the last scrub date from the command
'zpool status POOL'.

```

## Project pages

* https://github.com/Josef-Friedrich/check_zpool_scrub
* https://exchange.icinga.com/joseffriedrich/check_zpool_scrub
* https://exchange.nagios.org/directory/Plugins/System-Metrics/File-System/check_zpool_scrub/details

## Testing

```
make test
```

