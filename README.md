[![Build Status](https://travis-ci.org/Josef-Friedrich/check_zpool_scrub.svg?branch=master)](https://travis-ci.org/Josef-Friedrich/check_zpool_scrub)

# check_zpool_scrub


## Summary / Short description

> Monitoring plugin to check how long ago the last ZFS scrub was performed.

## Usage

```
check_zpool_scrub v1.1
Copyright (c) 2016-2018 Josef Friedrich <josef@friedrich.rocks>

Monitoring plugin to check how long ago the last ZFS scrub was performed.


Usage: check_zpool_scrub <options>

Options:
 -c, --critical=OPT_CRITICAL
    Interval in seconds for critical state.
 -p,--pool=OPT_POOL
    Name of the pool
 -h, --help
    Show this help.
 -r, --sudo
    Run 'zpool history' with the help of sudo.
 -s, --short-description
    Show a short description / summary.
 -v, --version
    Show the version number.
 -w, --warning=OPT_WARNING
    Interval in seconds for warning state. Must be lower than -c.

Performance data:
 - last_ago
    Time interval in seconds for last scrub.
 - warning
    Interval in seconds.
 - critical
    Interval in seconds.
 - progress
    Percent 0 - 100
 - speed
    MB per second
 - time
    Time to go in minutes

```

## Project pages

* https://github.com/Josef-Friedrich/check_zpool_scrub
* https://exchange.icinga.com/joseffriedrich/check_zpool_scrub
* https://exchange.nagios.org/directory/Plugins/System-Metrics/File-System/check_zpool_scrub/details

## Testing

```
make test
```

