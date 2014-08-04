from numpy import loadtxt, nan_to_num, zeros

import viscojapan as vj
from days_after_mainshock import days

sites = loadtxt("sites/sites", '4a')

num_sites = len(sites)
num_dates = len(days)

data = zeros([num_sites*3, num_dates])
for nth, site in enumerate(sites):
    tp = loadtxt('cumu_post_displacement/%s.cumu'%site.decode())
    for m in range(3):
        data[nth+m,:] = nan_to_num(tp[:,m+1])

ep = vj.EpochalData('cumu_post_predicted.h5')
ep['sites'] = sites
for day in days:
    tp = data[:,(day,)]
    print(tp.shape)
    ep[day] = tp
    
