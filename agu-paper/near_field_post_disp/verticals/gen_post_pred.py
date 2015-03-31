from os.path import join
import numpy as np

import viscojapan as vj

res_file = '../nrough_06_naslip_11.h5'

sites_file = '../sites_with_seafloor'

reader = vj.inv.ResultFileReader(res_file)

post = reader.get_pred_disp()
post = post.get_post_at_epoch(1344)

sites = [site.decode() for site in np.loadtxt(sites_file,'4a')]

sites = vj.sites_db.SitesDB().gets(sites)

with open('share/post_ver_1344_pred', 'wt') as fid:
    for d, s in zip(post, sites):
        lon = s.lon
        lat = s.lat
        fid.write('%f %f %f %f %s\n'%(lon, lat, 0, d[2], s))
