import numpy as np

import viscojapan as vj

sites = vj.utils.as_string(np.loadtxt('share/sites_with_seafloor', '4a',usecols=(0,)))

sites = vj.sites_db.SitesDB().gets(ids=sites)

sites_sorted, dist_sorted = vj.sites.sorted_by_epicentral_distance(
    sites,
    reverse=True)

cutoff = 600.

with open('share/sites_far', 'wt') as fid:
    for site, dist in zip(sites_sorted, dist_sorted):
        if dist > cutoff:
            fid.write('%s  %f\n'%(site, dist))
