from viscojapan.plots import plt, MapPlotDisplacement, MapPlotFault, MyBasemap
from viscojapan.epochal_data import EpochalG

fno = 120

scale = .0003
epoch = 1200
U = 2e-6
bm = MyBasemap(
    region_code = 'H',
    )

G50km = EpochalG('../G_He45km.h5')

disp0 = G50km.get_epoch_value(0)[:,fno]
disp1 = G50km.get_epoch_value(epoch)[:,fno]


mplt = MapPlotDisplacement(basemap = bm)

label = '%.1g co'%U
mplt.plot_disp(disp0, G50km.sites,
               X=0.1, Y=0.2,
               U=U, label=label, color='black', scale=scale)

label = '%.1g post'%U
mplt.plot_disp(disp1, G50km.sites,
               X=0.1, Y=0.1,
               U=U, label=label, color='red', scale=scale)

##mplt.plot_G_file('../G_He45km.h5', epoch, fno, scale=scale)
##mplt.plot_G_file('../G_He55km.h5', epoch, fno,
##                 color='red', scale=scale)

mplt = MapPlotFault('../../fault_model/fault_He50km.h5', basemap = bm)
mplt.plot_fault(fno)

plt.show()
