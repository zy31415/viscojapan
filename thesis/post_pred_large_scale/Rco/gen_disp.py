import numpy as np

import viscojapan as vj

pred_db='../../../inversions/inversion10/iter2/run7/analysis/pred_disp_large_scale/~pred_disp.db'

reader = vj.inv.PredDispToDatabaseReader(pred_db)
sites, ys = reader.get_R_co_at_epoch(1344)

tp = np.loadtxt('stations_large_scale.in','4a, f, f')
pos_dic = {ii[0].decode():(ii[1], ii[2]) for ii in tp}

with open('Rco','wt') as fid:
    for site, y in zip(sites, ys):
        lon, lat = pos_dic[site]
        mag = np.sqrt(y[0]**2+y[1]**2)
        fid.write('%f %f %f\n'%(lon, lat, mag))
