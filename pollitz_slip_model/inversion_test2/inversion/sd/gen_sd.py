import  numpy as np

import viscojapan as vj

sites = np.loadtxt('../sites_with_seafloor','4a')

gen = vj.tsana.GenOzawaSD(sites=sites, days=range(0,1201),
                          sd_seafloor = 1e99)
gen.save('sd_ozawa.h5')
