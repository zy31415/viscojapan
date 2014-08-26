import h5py
import numpy as np
from pylab import plt

import viscojapan as vj

sites_file = '../../sites_with_seafloor'
sites = np.loadtxt(sites_file, '4a')

res_file = '../outs/nsd_03_rough_10_top_02.h5'

d_obs = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5',
                               sites_file)[0]

with h5py.File(res_file,'r') as fid:
    Bm = fid['Bm'][...]
    d_pred = fid['d_pred'][...]


pltd = vj.PlotCoseismicDisp(
    d_obs = d_obs,
    d_pred = d_pred,
    sites = sites,
    fault_file = '../../fault_bott40km.h5',
    fault_slip = Bm
    )

for region_code in vj.region_ranges.keys():
    print(region_code)
    pltd.plot_at(region_code)
    plt.savefig('plots_disp/' + region_code +'.png')
    plt.close()

sites_file_far_field = 'sites_far_field'
sites_far_field = np.loadtxt(sites_file_far_field, '4a')

pltd.plot_far_field(sites_far_field)
plt.savefig('plots_disp/far_field.png')
plt.close()
