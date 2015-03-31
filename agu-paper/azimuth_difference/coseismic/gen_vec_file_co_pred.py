from os.path import join
import numpy as np

import viscojapan as vj

base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run2_seafloor_01/outs/nrough_14_ntop_02.h5')

sites_file = join(base_dir, 'coseismic/run2_seafloor_01/sites_with_seafloor')

reader = vj.inv.ResultFileReader(res_file)
d_pred = reader.d_pred.reshape([-1,3])
sites_pos = np.loadtxt(sites_file,'4a, f, f')

with open('co_pred', 'wt') as fid:
    for d, s in zip(d_pred, sites_pos):
        fid.write('%f %f %f %f %s\n'%(s[1], s[2], d[0], d[1], s[0].decode()))
