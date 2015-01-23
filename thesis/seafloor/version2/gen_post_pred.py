from os.path import join
import numpy as np

import viscojapan as vj

base_dir = '/home/zy/workspace/viscojapan/inversions/inversion10/iter2/run7/'
res_file = join(
    base_dir,
    'outs/nrough_05_naslip_11.h5')

sites_file = join(base_dir, 'sites_with_seafloor')

reader = vj.inv.DispResultReader(res_file)
post = reader.get_post_pred_at_epoch(1344)

sites = [site.decode() for site in np.loadtxt(sites_file,'4a')]

pos_dic = vj.sites_db.get_pos_dic()

with open('post_1344_pred', 'wt') as fid:
    for d, s in zip(post, sites):
        lon, lat = pos_dic[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))
