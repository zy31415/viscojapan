from os.path import join

import numpy as np

import viscojapan as vj

base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run2_seafloor_01/outs/nrough_14_ntop_02.h5')

G_file = join(
    base_dir,
    'green_function_china_korea/G5_He63km_VisM1.0E19_Rake83.h5')

reader = vj.ResultFileReader(res_file)

slip = reader.slip

reader = vj.EpochalFileReader(G_file)
G = reader[0]
sites = reader['sites']
sites = vj.Sites([site.decode() for site in sites])

d_pred = np.dot(G,slip).reshape([-1,3])

with open('disp','wt') as fid:
    for d, site in zip(d_pred, sites):
        fid.write('%f %f %f %f 0. 0. 0. %s\n'%\
                  (site.lon, site.lat, d[0], d[1], site.name))
        
