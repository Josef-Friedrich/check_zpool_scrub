#!/bin/sh

_zpool_status () {
echo '  pool: zfsdata
 state: ONLINE
  scan: scrub in progress since Sat Aug  3 10:21:02 2019
        461G scanned at 120M/s, 258G issued at 67.2M/s, 496G total
        0B repaired, 52.05% done, 0 days 01:03:21 to go
config:

        NAME                                       STATE     READ WRITE CKSUM
        zfsdata                                    ONLINE       0     0     0
          mirror-0                                ONLINE       0     0     0
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)
            ata-SanDisk_SDSSD            ONLINE       0     0     0  (trimming)'

}


_grab_time_to_go() {
  local MINUTES HOURS DAYS
  _get_line() {
    _zpool_status | grep ' to go'
  }
  if [ -n "$(_zpool_status | grep 'days .*:.*:.*')" ]; then
    DAYS="$(_get_line | sed -E 's/^.* (.*) days .*$/\1/g')"
    HOURS="$(_get_line | sed -E 's/^.*days (..):.*$/\1/g')"
    MINUTES="$(_get_line | sed -E 's/^.*days ..:(..):.*$/\1/g')"
    echo $((DAYS * 1440 + HOURS * 60 + MINUTES))
	elif [ -n "$(_zpool_status | grep 'h.*m) to go')" ]; then
    HOURS=$(_get_line | sed 's/h.*//')
    MINUTES=$(_get_line | sed 's/.*h//' | sed 's/m//')
    echo $((HOURS * 60 + MINUTES))
	else
		echo 0
	fi
}


_grab_time_to_go
