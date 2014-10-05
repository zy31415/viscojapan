import numpy as np

import viscojapan as vj

days = np.asarray(range(0,1201))

sites = np.loadtxt('stations.in','4a',usecols=(0,))

num_sites = len(sites)

sd = np.hstack((np.ones((num_sites,1)),
                np.ones((num_sites,1)),
                np.ones((num_sites,1))*5.))

ch = vj.choose_inland_GPS(sites)
sd[~ch,:] = 1e99

sd = sd.reshape([-1,1])

ep = vj.EpochalData('sd_hor_1_ver_5_sea_inf.h5')

for day in days:
    ep[int(day)] = sd

ep['sites'] = sites
