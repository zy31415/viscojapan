import numpy as np
from pylab import plt

import viscojapan as vj

tp = np.loadtxt('ozawa_2011_obs_file','4a,3f')
sites = [ii[0] for ii in tp]
disp0 = np.asarray([ii[1] for ii in tp]).flatten()

bm = vj.MyBasemap(region_code='D')
ep = vj.EpochalDisplacement('cumu_post_with_seafloor.h5',
                               filter_sites=sites)
disp1 = ep[0]
mplt = vj.MapPlotDisplacement(basemap=bm)

scale = 15
mplt.plot_disp(disp1, sites,scale=scale,
               X=0.2, Y=0.8, U=1, label='yang 1m')

mplt.plot_disp(disp0, sites,scale=scale,
               X=0.2, Y=0.9, U=1, label='ozawa 1m', color='red')

mplt = vj.MapPlotSlab(basemap=bm)
mplt.plot_top()
plt.savefig('compare.pdf')
plt.show()
