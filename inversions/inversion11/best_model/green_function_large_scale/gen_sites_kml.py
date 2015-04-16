import viscojapan as vj

import numpy as np

tp = np.loadtxt('stations_large_scale.in', '4a, f, f')

sites = []
for s, lon, lat in tp:
    site = vj.Site(s.decode(), lon, lat)
    sites.append(site)
sites  = vj.sites.Sites(sites)

vj.sites.save_sites_to_kml(sites, fn='stations_large_scale.kml')
