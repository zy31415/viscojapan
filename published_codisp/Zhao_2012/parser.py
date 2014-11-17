import numpy as np

import viscojapan as vj


tp = np.loadtxt('Zhao_2012_CMONOC.txt',
                'f, f, 4a',
                usecols=(2,3,6))

obs_dic = {ii[2].decode():(ii[0],ii[1]) for ii in tp}

tp = np.loadtxt('Zhao_2012_IGS.txt',
                'f, f, 4a',
                usecols=(2,3,6))

for ii in tp:
    obs_dic[ii[2].decode()] = (ii[0],ii[1])


with open('zhao_2012_obs','wt') as fid:
    for k,v in obs_dic.items():
        fid.write('%s %f %f\n'%\
                  (k, v[0]/1e3, v[1]/1e3))
    
