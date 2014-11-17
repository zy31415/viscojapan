import numpy as np

import viscojapan as vj


tp = np.loadtxt('Baek_2012_supp_TableS1.txt',
                'a5, f, f, f, f',
                usecols=(0,1,2,3,6))
# note the the publication got the unit wrong.

with open('baek_2012_obs','wt') as fid:
    for ii in tp:
        site = ii[0].decode()
        if len(site)==5:
            site = site[1:]
        fid.write('%s %f %f\n'%\
                  (site, ii[3]/1e2, ii[4]/1e2, ))
    
