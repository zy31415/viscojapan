import numpy as np

import viscojapan as vj

tp = np.loadtxt('../../../published_codisp/china_codisp','4a,f,f')
sites = [ii[0].decode() for ii in tp]

pos = vj.sites_db.get_pos_dic()

with open('china_obs.in','wt') as fid:
    for ii in tp:
        site = ii[0].decode()
        lon, lat = pos[site]
        fid.write('%f %f %f %f 0. 0. 0. %s\n'%\
                  (lon, lat, ii[1], ii[2], site)
                  )
                  

tp = np.loadtxt('../disp','4f, 4a', usecols=(0,1,2,3,7))
pred_dic = {ii[1].decode():ii[0] for ii in tp}

with open('china_pred.in', 'wt') as fid:
    for site in sites:
        tp = pred_dic[site]
        fid.write('%f %f %f %f 0. 0. 0. %s\n'%\
                  (tp[0], tp[1], tp[2], tp[3], site)
                  )
    
