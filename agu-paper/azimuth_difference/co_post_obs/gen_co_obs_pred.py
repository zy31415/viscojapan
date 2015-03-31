import numpy as np

import viscojapan as vj

#########################################
# gen obs

reader = vj.inv.ep.EpochDisplacement('../cumu_post_with_seafloor.h5')
co = reader.get_coseismic_disp()
post = reader.get_post_at_epoch(1344)

sites = reader.get_mask_sites()
pos = vj.sites_db.get_pos_dic()

with open('share/co_obs', 'wt') as fid:
    for d, s in zip(co, sites):
        lon, lat = pos[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))

with open('share/post_1344_obs', 'wt') as fid:
    for d, s in zip(post, sites):
        lon, lat = pos[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))


