import numpy as np

days = np.asarray(range(0,1201))

import viscojapan as vj

sites = np.loadtxt('sites_with_seafloor', '4a',usecols=(0,))

gen = vj.tsana.GenUniformSD(
    sites = sites,
    days = days,
    sd_seafloor = 1e99,
    sd_inland = 1.,
    sd_co = 0.01,
    )

gen.save('sd_uniform_co.h5')
