import numpy as np

import viscojapan as vj

pred='/home/zy/workspace/viscojapan/inversions/inversion10/iter2/run7/analysis/pred_disp_large_scale/partition_large_scale.h5'

reader = vj.inv.DeformPartitionResultReader(pred)
Ecumu = reader.Ecumu

post = Ecumu.get_post_at_nth_epoch(-1)

sites = Ecumu.sites

tp = np.loadtxt('stations_large_scale.in','4a, f, f')
pos_dic = {ii[0].decode():(ii[1], ii[2]) for ii in tp}

with open('Easlip','wt') as fid:
    for site, y in zip(sites, post):
        lon, lat = pos_dic[site.id]
        mag = np.sqrt(y[0]**2+y[1]**2)
        fid.write('%f %f %f\n'%(lon, lat, mag))
