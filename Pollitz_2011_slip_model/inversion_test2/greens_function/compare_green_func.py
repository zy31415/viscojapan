import h5py
from pylab import plt

import viscojapan as vj

point_source_file = './G_He63km_Rake81.h5'

reg_source_file = '../../../inversions/static_inversion/greens_function/G_He63km_Rake81.h5'

fault_file = '../fault_model/fault_bott50km.h5'

with h5py.File(point_source_file) as fid:
    G0 = fid['epochs/0000'][...]
    sites = fid['info/sites'][...]

with h5py.File(reg_source_file) as fid:
    G1 = fid['epochs/0000'][...]

#nth = 34
nth = 0

disp0 = G0[:,nth]
disp1 = G1[:,nth]


#scale = 8e-4
scale = 2e-5

bm = vj.MyBasemap(region_code='I')

mplt = vj.MapPlotDisplacement(basemap=bm)
mplt.plot_disp(disp0, sites, scale=scale,
               X=0.2, Y=0.8, U=1e-6, label='point source')
mplt.plot_disp(disp1, sites,color='r', scale=scale,
               X=0.2, Y=0.9, U=1e-6, label='reg source')

mplt = vj.MapPlotFault(fault_file,basemap=bm)
mplt.plot_fault(fno=nth)

plt.show()
