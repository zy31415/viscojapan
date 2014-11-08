#!/bin/bash
sqlite3 gps_sites.db <<!
.headers on
.output database_backup.schema
.schema
!

sqlite3 gps_sites.db <<!
.headers on
.output database_backup.data
.dump
!
