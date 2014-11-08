#!/bin/bash
rm -f database_backup.schema
sqlite3 gps_sites.db <<!
.headers on
.output database_backup.schema
.schema
!

rm -f database_backup.data
sqlite3 gps_sites.db <<!
.headers on
.output database_backup.data
.dump
!
