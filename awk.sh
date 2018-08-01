#! /bin/sh

# echo 'pool: data
# state: ONLINE
# scan: scrub in progress since Sun Aug 13 00:24:02 2017
# 7,34T scanned out of 10,1T at 57,4M/s, 14h12m to go
# 0 repaired, 72,38% done' | \
#         grep ' to go' |
#         sed  '/\(m\)/\1/'

echo 'pool: data
state: ONLINE
scan: scrub in progress since Sun Aug 13 00:24:02 2017
7,34T scanned out of 10,1T at 57,4M/s, 14h12m to go
0 repaired, 72,38% done' | \
        grep ' to go' |
        awk '{ print $8 }'
