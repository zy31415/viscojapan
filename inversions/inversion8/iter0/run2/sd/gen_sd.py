import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites_with_seafloor',
                   '4a',usecols=(0,))

gen = vj.tsana.GenUniformOnshoreSDWithInfiniteSeafloorSD(
    sites = sites,
    days = range(0,1300),
    sd_co_hor = 1,
    sd_co_ver = 5,
    sd_post_hor = 3,
    sd_post_ver = 15, 
    )

gen.save('sd_uniform.h5')

vj.tsana.copy_and_revise_sd_file(
    'sd_uniform.h5',
    'seafloor_sd',
    'sd_uniform_seafloor_inf.h5',
    [1e99]*3)
