import h5py
import numpy as np
from pylab import plt

import viscojapan as vj
from viscojapan.plots.plot_coseismic_disp import PlotCoseismicDisp

sites_file = '../../sites_with_seafloor'
sites = np.loadtxt(sites_file, '4a')

res_file = '../outs/nsd_03_rough_10_top_02.h5'

d_obs = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5',
                               sites_file)[0]


with h5py.File(res_file,'r') as fid:
    Bm = fid['Bm'][...]
    d_pred = fid['d_pred'][...]


pltd = PlotCoseismicDisp(
    d_obs = d_obs,
    d_pred = d_pred,
    sites = sites,
    fault_file = '../../fault_bott40km.h5',
    fault_slip = Bm
    )

pltd.plot_at_all()              
plt.show()
