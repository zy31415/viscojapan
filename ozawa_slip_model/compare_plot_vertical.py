import numpy as np
from pylab import plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

import viscojapan as vj

tp = np.loadtxt('ozawa_2011_obs_file','4a,3f')
sites = [ii[0] for ii in tp]
disp0 = np.asarray([ii[1] for ii in tp]).flatten()
us0 = disp0[2::3]

ep = vj.EpochalDisplacement('cumu_post_with_seafloor.h5',
                            filter_sites=sites)
disp1 = ep[0]
us1 = disp1[2::3]

plt.subplot(121)
bm = vj.MyBasemap(region_code='near')
mplt = vj.MapPlotDisplacement(basemap=bm)
mplt.plot_scalor(us0, sites, cmap='RdBu')
mplt = vj.MapPlotSlab(basemap=bm)
mplt.plot_top()
plt.clim([-1., 1.])

plt.subplot(122)
bm = vj.MyBasemap(region_code='near')
mplt = vj.MapPlotDisplacement(basemap=bm)
im = mplt.plot_scalor(us1, sites, cmap='RdBu')
mplt = vj.MapPlotSlab(basemap=bm)
mplt.plot_top()
plt.clim([-1., 1.])

divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="5%", pad=0.05)
plt.colorbar(im, cax=cax)

plt.savefig('compare.pdf')
plt.show()
