import numpy as np

days = np.asarray(range(0,1201))

import viscojapan as vj

sites = np.loadtxt('sites_with_seafloor', '4a',usecols=(0,))

gen = vj.tsana.GenUniformSD(
    sites = sites,
    days = days,
    sd_seafloor = 100.,
    sd_inland = 1., 
    )

gen.save('sd_uniform.h5')
