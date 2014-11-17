import numpy as np

import viscojapan as vj


tp = np.loadtxt('Wang_2011_TEONET.txt',
                'a5, f, f, f, f',
                usecols=(0,1,2,3,6))

obs_dic = {ii[0].decode():(ii[3],ii[4]) for ii in tp}

tp = np.loadtxt('Wang_2011_IGS.txt',
                'a5, f, f, f, f',
                usecols=(0,1,2,3,6))

for ii in tp:
    obs_dic[ii[0].decode()] = (ii[3],ii[4])


with open('wang_2011_obs','wt') as fid:
    for k,v in obs_dic.items():
        fid.write('%s %f %f\n'%\
                  (k, v[0], v[1]))
    
