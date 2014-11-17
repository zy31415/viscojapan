import numpy as np

import viscojapan as vj


tp = np.loadtxt('Baek_2012_supp_TableS1.txt',
                'a5, f, f, f, f',
                usecols=(0,1,2,3,6))

with open('baek_2012_obs','wt') as fid:
    for ii in tp:
        fid.write('%f %f %f %f 0. 0. 0. %s\n'%\
                  (ii[1], ii[2], ii[3]/1e2, ii[4]/1e2, ii[0].decode()))
    
