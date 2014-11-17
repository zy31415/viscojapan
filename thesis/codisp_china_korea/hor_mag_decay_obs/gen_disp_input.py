import numpy as np

import viscojapan as vj

tp = np.loadtxt('/home/zy/workspace/viscojapan/published_codisp/all_published_codisp',
                '4a, f, f')
published = {ii[0].decode():np.asarray((ii[1],ii[2]),float)
           for ii in tp}

# Read from my estimation
reader = vj.EpochalFileReader('../../../tsana/post_fit/cumu_post.h5')

disp = reader[0].reshape([-1,3])
sites = reader['sites']

mine = {s.decode():d[:-1] for s, d in zip(sites, disp)}

obs_dic = vj.merge_disp_dic(published, mine)

allpos = vj.sites_db.get_pos_dic()

with open('obs_hor_mag','wt') as fid:
    for site,pos in obs_dic.items():
        lon, lat = allpos[site]
        fid.write('%f %f %f\n'%\
                  (lon, lat, np.sqrt(pos[0]**2+pos[0]**2)))
