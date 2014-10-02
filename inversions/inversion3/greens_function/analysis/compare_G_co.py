import numpy as np

from viscojapan.plots import plt, MapPlotDisplacement, MapPlotFault, MyBasemap
from viscojapan.epochal_data import EpochalG

fno = 30
scale = .0009
epoch = 1200
U = 1e-6
label='%.1G'%U

bm = MyBasemap(
    region_code = 'near',
    )

sites = np.loadtxt('sites_without_seafloor','4a,', usecols=(0,))

G45km = EpochalG('../G_He45km.h5', filter_sites=sites)
G50km = EpochalG('../G_He50km.h5', filter_sites=sites)
G55km = EpochalG('../G_He55km.h5', filter_sites=sites)

d0_45km = G45km.get_epoch_value(0)[:,fno]
d_45km = G45km.get_epoch_value(epoch)[:,fno]

d0_50km = G50km.get_epoch_value(0)[:,fno]
d_50km = G50km.get_epoch_value(epoch)[:,fno]

d0_55km = G55km.get_epoch_value(0)[:,fno]
d_55km = G55km.get_epoch_value(epoch)[:,fno]

mplt = MapPlotDisplacement(basemap = bm)

mplt.plot_disp(d0_45km, sites,
               U = U, label = label+'-45km',
               X=0.1, Y=0.9,
               color='black', scale=scale)

mplt.plot_disp(d0_50km, sites,
               U = U, label = label+'-50km',
               X=0.1, Y=0.8,
               color='blue', scale=scale)

mplt.plot_disp(d0_55km, sites,
               U = U, label = label+'-55km',
               X=0.1, Y=0.7,
               color='red', scale=scale)
##mplt.plot_G_file('../G_He45km.h5', epoch, fno, scale=scale)
##mplt.plot_G_file('../G_He55km.h5', epoch, fno,
##                 color='red', scale=scale)

mplt = MapPlotFault('../../fault_model/fault_He50km.h5', basemap = bm)
mplt.plot_fault(fno)
plt.savefig('compare.pdf')
plt.show()
