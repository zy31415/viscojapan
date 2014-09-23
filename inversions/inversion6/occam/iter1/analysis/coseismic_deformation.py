from pylab import plt
import numpy as np

import viscojapan as vj
##
sites = np.loadtxt('../sites','4a')
##ep = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5','../sites')
##slip_co = ep[0]
##
##
##mplt = vj.MapPlotDisplacement()
##
##mplt.plot_disp(slip_co,sites)
##plt.show()


ep = vj.EpochalSlip('../slip0/incr_slip0.h5')
slip_co = ep[0]

mplt = vj.MapPlotFault('../fault_model/fault_bott50km.h5')
mplt.plot_slip(slip_co)

plt.show()
