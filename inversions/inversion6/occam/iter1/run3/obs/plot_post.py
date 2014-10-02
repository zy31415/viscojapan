from pylab import plt
import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites', '4a')

ep = vj.EpochalDisplacement('post_obs.h5', filter_sites = sites)

bm = vj.MyBasemap(region_code='E')

mplt = vj.MapPlotDisplacement(bm)

scale=.0007
disp = ep[1]
mplt.plot_disp(disp, sites, color='red', scale=scale,
               X=0.8, Y=0.9, U=0.0001, label='0.1mm, 1 day')

scale = .5
disp = ep[1199]
mplt.plot_disp(disp, sites, scale=scale,
               X=0.8, Y=0.8, U=.05, label='5cm, 1199 day')
#mplt.plot_sites(sites)

plt.savefig('post_disp.pdf')
plt.show()
