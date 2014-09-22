import h5py
import numpy as np
from pylab import plt

import viscojapan as vj


reg_source_file = '../../../inversions/static_inversion/greens_function/G_He63km_Rake81.h5'

fault_file = '../fault_model/fault_bott50km.h5'

with h5py.File(reg_source_file) as fid:
    G1 = fid['epochs/0000'][...]
    sites = fid['info/sites'][...]

#nth = 34
nth = 15

point_source_file = './outs_He63km_Rake81/day_0000_flt_%04d.out'%nth

tp = np.loadtxt(point_source_file)
disp0 = tp[:,2:5].flatten()

disp1 = G1[:,nth]


#scale = 2e-3
scale = 4e-5

bm = vj.MyBasemap(region_code='I')

mplt = vj.MapPlotFault(fault_file,basemap=bm)
mplt.plot_fault(fno=nth)

mplt = vj.MapPlotDisplacement(basemap=bm)
mplt.plot_disp(disp0, sites, scale=scale,
               X=0.2, Y=0.8, U=1e-6, label='point source')
mplt.plot_disp(disp1, sites,color='r', scale=scale,
               X=0.2, Y=0.9, U=1e-6, label='reg source')



plt.savefig('~compare.pdf')
plt.show()
