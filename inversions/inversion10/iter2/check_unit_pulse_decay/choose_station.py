import viscojapan as vj

import numpy as np

sites = vj.sites_db.SitesDB().gets_from_txt_file('stations.in')

sites_sorted, dist_sorted = vj.sites.sorted_by_epicentral_distance(sites)

sites_sorted[0:100].save_to_txt('near_stations.in')
