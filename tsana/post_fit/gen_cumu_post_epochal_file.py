from numpy import loadtxt, nan_to_num, zeros

import h5py

import viscojapan as vj
from days_after_mainshock import days

sites = loadtxt("sites/sites_with_seafloor", '4a', usecols=(0,))


num_sites = len(sites)
num_dates = len(days)

data = zeros([num_dates, num_sites, 3])
for nth, site in enumerate(sites):
    tp = loadtxt('cumu_post_displacement/%s.cumu'%site.decode())
    data[:,nth,:] = tp[:,1:]

epochs = list(tp[:,0])

with h5py.File('cumu_post_with_seafloor.h5','w') as fid:
    fid['data3d'] = nan_to_num(data)
    fid['epochs'] = epochs
    fid['sites'] = sites

    
