from viscojapan.plots import plt, MapPlotDisplacement, MapPlotFault, MyBasemap
from viscojapan.epochal_data import EpochalG

fno = 120
scale = .00003
epoch = 1200
U = 1e-6
label='%.1G'%U

bm = MyBasemap(
    region_code = 'E',
    )

G45km = EpochalG('../G_He45km.h5')
G55km = EpochalG('../G_He55km.h5')

d0_45km = G45km.get_epoch_value(0)[:,fno]
d_45km = G45km.get_epoch_value(epoch)[:,fno]

d0_55km = G55km.get_epoch_value(0)[:,fno]
d_55km = G55km.get_epoch_value(epoch)[:,fno]

mplt = MapPlotDisplacement(basemap = bm)

mplt.plot_disp(d_45km - d0_45km, G45km.sites,
               U = U, label = label,
               X=0.1, Y=0.8,
               color='black', scale=scale)

mplt.plot_disp(d_55km - d0_55km, G55km.sites,
               U = U, label = label,
               X=0.1, Y=0.7,
               color='red', scale=scale)
##mplt.plot_G_file('../G_He45km.h5', epoch, fno, scale=scale)
##mplt.plot_G_file('../G_He55km.h5', epoch, fno,
##                 color='red', scale=scale)

mplt = MapPlotFault('../../fault_model/fault_He50km.h5', basemap = bm)
mplt.plot_fault(fno)

plt.show()
