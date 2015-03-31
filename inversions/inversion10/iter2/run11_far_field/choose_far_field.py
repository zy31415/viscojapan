import numpy as np

import viscojapan as vj

sites = vj.utils.as_string(np.loadtxt('sites_with_seafloor', '4a',usecols=(0,)))

sites = vj.sites_db.SitesDB().gets(ids=sites)

sites_sorted, dist_sorted = vj.sites.sorted_by_epicentral_distance(sites)

ch = np.asarray(dist_sorted)>600

sites_ch = np.asarray(sites_sorted)[ch]

sites_ch = sorted([site.id for site in sites_ch] )

with open('sites_far', 'wt') as fid:
    for site in sites_ch:
        fid.write('%s\n'%site)
