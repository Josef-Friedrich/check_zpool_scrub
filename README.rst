.. image:: http://img.shields.io/pypi/v/check-zpool-scrub.svg
    :target: https://pypi.org/project/check-zpool-scrub
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/check_zpool_scrub/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/check_zpool_scrub/actions/workflows/tests.yml
    :alt: Tests

Command line interface
----------------------

:: 

    usage: check_zpool_scrub [-h] [-c CRITICAL] [-p POOL] [-s SHORT_DESCRIPTION]
                             [-v] [-w WARNING]

    Copyright (c) 2016-22 Josef Friedrich <josef@friedrich.rocks>

    Monitoring plugin to check how long ago the last ZFS scrub was performed.

    options:
      -h, --help            show this help message and exit
      -c CRITICAL, --critical CRITICAL
                            Interval in seconds for critical state.
      -p POOL, --pool POOL  Name of the pool. If this option is omitted all pools
                            are checked.
      -s SHORT_DESCRIPTION, --short-description SHORT_DESCRIPTION
                            Show a short description / summary.
      -v, --version         show program's version number and exit
      -w WARNING, --warning WARNING
                            Interval in seconds for warning state. Must be lower
                            than -c.

    Performance data:

    POOL is the name of the pool

     - POOL_last_ago
        Time interval in seconds for last scrub.
     - POOL_progress
        Percent 0 - 100
     - POOL_speed
        MB per second.
     - POOL_time
        Time to go in seconds.

    Details about the implementation of this monitoring plugin:

    This monitoring plugin grabs the last scrub date from the command
    'zpool status POOL'.

