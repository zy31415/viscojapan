from pylab import plt
import numpy as np

import viscojapan as vj

mplt = vj.MapPlotSlab()
mplt.plot_top()

tp = np.loadtxt('/home/zy/workspace/viscojapan/Pollitz_slip_model/Pollitz-slipmodel.txt')
lons = tp[:,0].reshape((42,-1))
lats = tp[:,1].reshape((42,-1))

mplt.basemap.plot(lons,lats, color='green', latlon=True)
mplt.basemap.plot(np.ascontiguousarray(lons.T),np.ascontiguousarray(lats.T), color='green', latlon=True)

mplt = vj.MapPlotFault('fault_bott50km.h5')
mplt.plot_fault(color='red')

plt.show()

