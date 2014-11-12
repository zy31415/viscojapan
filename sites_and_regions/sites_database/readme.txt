In this directory, I generate the site database, which has information about
site position and network information.
Two steps:
(1) run gen_sites_database.py to generate gps_sites.db.
(2) run select_GEONET_stations.py to set all GEONET stations.

Finally, use backup.sh to backup the database and use git to track the database.

2011, Nov 7
