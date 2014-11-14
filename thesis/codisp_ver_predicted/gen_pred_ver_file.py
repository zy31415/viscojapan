from os.path import join

import numpy as np

import viscojapan as vj

base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run2_seafloor_01/outs/nrough_14_ntop_02.h5')

sites_file = join(base_dir, 'coseismic/run2_seafloor_02/sites_with_seafloor')

reader = vj.ResultFileReader(res_file)
d_pred = reader.d_pred.reshape([-1,3])
sites_pos = np.loadtxt(sites_file,'4a, f, f')

assert len(sites_pos) == d_pred.shape[0]

_txt = np.array([(s[1],s[2],abs(d[2]),s[0]) for s, d in zip(sites_pos, d_pred)],
                ('f,f,f,U4'))
np.savetxt('pred_vertical',_txt, '%f %f %f %s')
