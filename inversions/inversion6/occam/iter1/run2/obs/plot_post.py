from pylab import plt
import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites', '4a')

ep = vj.EpochalDisplacement('post_obs.h5', filter_sites = sites)
disp = ep[1]

mplt = vj.MapPlotDisplacement()
mplt.plot_disp(disp, sites)

plt.show()
