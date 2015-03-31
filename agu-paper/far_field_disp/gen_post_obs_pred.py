import numpy as np

import viscojapan as vj

#########################################
# gen obs

reader = vj.inv.ep.EpochDisplacement('cumu_post_with_seafloor.h5')
post = reader.get_post_at_epoch(1344)

sites = reader.get_mask_sites()
pos = vj.sites_db.get_pos_dic()

sites_far = vj.utils.as_string(np.loadtxt('share/sites_far','4a', usecols=(0,)))

with open('share/post_1344_obs', 'wt') as fid:
    for d, s in zip(post, sites):
        if s in sites_far:
            lon, lat = pos[s]
            fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))


#########################################
# gen prediction
res_file = 'nrough_06_naslip_11.h5'

sites_file = 'share/sites_with_seafloor'

reader = vj.inv.ResultFileReader(res_file)

post = reader.get_pred_disp()
post = post.get_post_at_epoch(1344)

sites = [site.decode() for site in np.loadtxt(sites_file,'4a')]

sites = vj.sites_db.SitesDB().gets(sites)

sites_far = vj.utils.as_string(np.loadtxt('share/sites_far','4a', usecols=(0,)))

with open('share/post_1344_pred', 'wt') as fid:
    for d, s in zip(post, sites):
        if s.id in sites_far:
            lon = s.lon
            lat = s.lat
            fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s.id))
