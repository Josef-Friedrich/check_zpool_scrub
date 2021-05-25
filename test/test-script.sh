#!/bin/sh

_get_zpool_status_stdout () {
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


_speed() {
	local SPEED UNIT
	SPEED="$(_get_zpool_status_stdout "$1" | grep -E -o '[[:digit:],]*[[:alpha:]]/s')"
  echo $SPEED

	if [ -n "$SPEED" ]; then
    SPEED=$(echo "$1" | sed 's#/s##' | tr , .)
    UNIT=$(echo -n "$SPEED" | tail -c 1)
    SPEED=$(echo "$SPEED" | sed 's/.$//' )

    if [ "$UNIT" = K ]; then
      SPEED="$(echo "$SPEED" | \
        awk '{MB = $1 / 1024 ; print MB}')"
    fi
    echo $SPEED
	else
		echo 0
	fi
}

_speed
