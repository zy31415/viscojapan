from pylab import plt
import numpy as np

import viscojapan as vj

from epochs import epochs

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

##mplt = vj.MapPlotFault('../fault_model/fault_bott50km.h5')
##mplt.plot_slip(slip_co)

ep_obs = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5','../sites')

f_G = '../green_function/G_He50km_Vis5.8E18_Rake90.h5'
ep_co_disp = vj.EpochalG(f_G,filter_sites=sites)
for epoch in epochs:
    G = ep_co_disp[epoch]
    disp = np.dot(G, slip_co)
    disp_obs = ep_obs[epoch]

    mplt = vj.MapPlotDisplacement()
    mplt.plot_disp(disp_obs, sites, color='red')
    mplt.plot_disp(disp, sites)
    plt.title('%d'%epoch)
    plt.show()
