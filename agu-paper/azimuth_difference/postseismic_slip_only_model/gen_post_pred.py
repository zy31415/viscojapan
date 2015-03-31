from os.path import join
import numpy as np

import viscojapan as vj

base_dir = '/home/zy/workspace/viscojapan/inversions/inversion10/iter2/static_inversion/'
res_file_post = join(
    base_dir,
    'outs/outs_1344/rough_16.h5')

res_file_co = join(
    base_dir,
    'outs/outs_0000/rough_16.h5')


sites_file = join(base_dir, 'sites_with_seafloor')

reader = vj.inv.ResultFileReader(res_file_post)
d_cumu_post = reader.d_pred.reshape([-1,3])

reader = vj.inv.ResultFileReader(res_file_co)
d_co = reader.d_pred.reshape([-1,3])

d_post = d_cumu_post - d_co

sites = [site.decode() for site in np.loadtxt(sites_file,'4a')]

pos_dic = vj.sites_db.get_pos_dic()

with open('post_1344_pred', 'wt') as fid:
    for d, s in zip(d_post, sites):
        lon, lat = pos_dic[s]
        fid.write('%f %f %f %f %s\n'%(lon, lat, d[0], d[1], s))
