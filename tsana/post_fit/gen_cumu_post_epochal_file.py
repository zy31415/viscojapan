from numpy import loadtxt, nan_to_num, zeros

import viscojapan as vj
from days_after_mainshock import days

sites = loadtxt("sites/sites_with_seafloor", '4a', usecols=(0,))


num_sites = len(sites)
num_dates = len(days)

data = zeros([num_sites*3, num_dates])
for nth, site in enumerate(sites):
    tp = loadtxt('cumu_post_displacement/%s.cumu'%site.decode())
    for m in range(3):
        data[nth*3+m,:] = nan_to_num(tp[:,m+1])

with vj.EpochalFileWriter('cumu_post_with_seafloor.h5') as writer:
    writer['sites'] = sites
    for day in days:
        print(day)
        tp = data[:,(day,)]
        writer[int(day)] = tp
    
