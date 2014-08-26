import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites_with_seafloor','4a')

for code, rge in vj.region_ranges.items():
    if code =='all':
        continue
    tp = vj.get_sites_in_box(rge)
    sites = vj.remove_sites_from(sites, tp)

np.savetxt('sites_far_field',sorted([ii.decode() for ii in sites]),
           fmt='%s', header='far field sites.')
