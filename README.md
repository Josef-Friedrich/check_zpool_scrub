[![Build Status](https://travis-ci.org/JosefFriedrich-shell/check_zpool_scrub.svg?branch=master)](https://travis-ci.org/JosefFriedrich-shell/check_zpool_scrub)

# check_zpool_scrub

## Summary / Short description

> Monitoring plugin to check how long ago the last ZFS scrub was performed.

## Usage

```
check_zfs_scrub
Copyright (c) 2016 Josef Friedrich <josef@friedrich.rocks>

Monitoring plugin to check how long ago the last ZFS scrub was performed.


Usage: check_zfs_scrub <options>

Options:
  -c, --critical=INTERVAL_CRITICAL
    Interval in seconds for critical state.
  -p,--pool=POOL
    Name of the pool
  -h, --help
    Show this help.
  -s, --short-description
    Show a short description / summary.
  -w, --warning=INTERVAL_WARNING
    Interval in seconds for warning state. Must be lower than -c.
```

## Testing

```
make test
```
