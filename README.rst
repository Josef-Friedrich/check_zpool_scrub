.. image:: http://img.shields.io/pypi/v/check-zpool-scrub.svg
    :target: https://pypi.org/project/check-zpool-scrub
    :alt: This package on the Python Package Index

.. image:: https://github.com/Josef-Friedrich/check_zpool_scrub/actions/workflows/tests.yml/badge.svg
    :target: https://github.com/Josef-Friedrich/check_zpool_scrub/actions/workflows/tests.yml
    :alt: Tests

Note: This monitoring plugin is written in Python from version 3 onwards.
Earlier versions of this plugin were written in shell script. The latest version
of the shell script can be retrieved via the `git history
<https://github.com/Josef-Friedrich/check_zpool_scrub/tree/9fc9373f455a0e4980d87e936e2036c6041addf0>`__.

Command line interface
----------------------

:: 

    usage: check_zpool_scrub [-h] [-V] [-v] [-p POOL] [-w WARNING] [-c CRITICAL]
                             [-d]

    version 3.0.0a2
    Licensed under the MIT.
    Repository: https://github.com/Josef-Friedrich/check_zpool_scrub.
    Copyright (c) 2016-2026 Josef Friedrich <josef@friedrich.rocks>

    Monitoring plugin to check how long ago the last ZFS scrub was performed.

    options:
      -h, --help            show this help message and exit
      -V, --version         show program's version number and exit
      -v, --verbose         Increase output verbosity (use up to 3 times).
      -p, --pool POOL       Name of the pool. If this option is omitted all pools
                            are checked.
      -w, --warning WARNING
                            Interval in seconds for warning state. Must be lower
                            than -c.
      -c, --critical CRITICAL
                            Interval in seconds for critical state.
      -d, --debug           Increase debug verbosity (use up to 3 times): -D: info
                            -DD: debug. -DDD verbose

    Performance data:

    POOL is the name of the pool

     - POOL_last_scrub
        Time interval in seconds for last scrub.
     - POOL_progress
        Percent 0 - 100
     - POOL_speed
        MB per second.
     - POOL_time_to_go
        Time to go in seconds.

    Details about the implementation of this monitoring plugin:

    This monitoring plugin grabs the last scrub date from the command
    'zpool status POOL'.

Project pages
-------------

* https://github.com/Josef-Friedrich/check_zpool_scrub
* https://exchange.icinga.com/joseffriedrich/check_zpool_scrub
* https://exchange.nagios.org/directory/Plugins/System-Metrics/File-System/check_zpool_scrub/details
