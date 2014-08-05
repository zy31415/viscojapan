from numpy import loadtxt, nan_to_num, zeros

import viscojapan as vj
from days_after_mainshock import days

tp = loadtxt("sites/sites", '4a, 2f')
sites = [ii[0] for ii in tp]

num_sites = len(sites)
num_dates = len(days)

data = zeros([num_sites*3, num_dates])
for nth, site in enumerate(sites):
    tp = loadtxt('cumu_post_displacement/%s.cumu'%site.decode())
    for m in range(3):
        data[nth*3+m,:] = nan_to_num(tp[:,m+1])

ep = vj.EpochalData('cumu_post.h5')
ep['sites'] = sites
for day in days:
    print(day)
    tp = data[:,(day,)]
    ep[int(day)] = tp
    
