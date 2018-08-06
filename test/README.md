# Date conversion

## Formats

* datetime: 2017-07-17.10:25:48
* date: 2017-06-16
* ctime: Mon Jul 17 10:25:48 2017
* timestamp: 1502958348

## Date to Timestamp

```
date  +%s --date=DATE"
```

## Timestamp to Date

```
date  +"%Y-%m-%d %H:%M:%SZ --date=@TIMESTAMP"
```

# Calculations

```
now = 1502958348 (2017-08-17 10:25:48)
now - warning = 1502958348 - 2678400 = 1500279948 (2017-07-17 10:25:48)
now - critical = 1502958348 - 5356800 = 1497601548 (2017-06-16 10:25:48)
```

```
ok:       2017-08-17 10:25:48 - 2017-07-17 10:25:48
          1502958348            1500279948

warning:  2017-07-17 10:25:47 - 2017-06-16 10:25:48
          1500279947            1497601548

critical: 2017-06-16 10:25:47  ->
          1497601547
```

# Result

| Name     | Date                | Timestamp  |
|----------|---------------------|------------|
| now      | 2017-08-17 10:25:48 | 1502958348 |
| warning  | 2017-07-17 10:25:48 | 1500279948 |
| critical | 2017-06-16 10:25:48 | 1497601548 |

# Zpool names

* `last_ok_zpool`
* `last_warning_zpool`
* `first_critical_zpool`

# Dates chosen for testing

* `first_critical_zpool`: `1497601547` (`2017-06-16 10:25:47`) -> first critical date
* `last_warning_zpool`: `1497601548` (`2017-06-16 10:25:48`) -> last warning date
* `first_warning_zpool`: `1500279947` (`2017-07-17 10:25:47`) -> first warning date
* `last_ok_zpool`: `1500279948` (`2017-07-17 10:25:48`) -> last ok date
* `first_ok_zpool`: `1502958348` (`2017-08-17 10:25:48`) -> now
