import numpy as np

import viscojapan as vj

#########################################
# gen obs

reader = vj.inv.ep.EpochDisplacement('cumu_post_with_seafloor.h5')
post = reader.get_coseismic_disp()

sites = reader.get_mask_sites()
pos = vj.sites_db.get_pos_dic()

with open('share/co_obs', 'wt') as fid:
    for d, s in zip(post, sites):
        lon, lat = pos[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))


#########################################
# gen prediction
res_file = 'nrough_06_naslip_11.h5'

sites_file = 'sites_with_seafloor'

reader = vj.inv.ResultFileReader(res_file)

post = reader.get_pred_disp()
post = post.get_coseismic_disp()

sites = [site.decode() for site in np.loadtxt(sites_file,'4a')]

sites = vj.sites_db.SitesDB().gets(sites)

with open('share/co_pred', 'wt') as fid:
    for d, s in zip(post, sites):    
        lon = s.lon
        lat = s.lat
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s.id))
