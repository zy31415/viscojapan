import numpy as np

import viscojapan as vj

res_file='/home/zy/workspace/viscojapan/inversions/inversion10/iter2/run7/outs/nrough_05_naslip_11.h5'

reader = vj.inv.ResultFileReader(res_file)
disp = reader.get_pred_disp()

post = disp.get_post_at_nth_epoch(-1)

sites = disp.get_sites

tp = np.loadtxt('stations_large_scale.in','4a, f, f')
pos_dic = {ii[0].decode():(ii[1], ii[2]) for ii in tp}

with open('post_disp2','wt') as fid:
    for site, y in zip(sites, post):
        lon, lat = pos_dic[site.id]
        mag = np.sqrt(y[0]**2+y[1]**2)
        fid.write('%f %f %f\n'%(lon, lat, mag))
