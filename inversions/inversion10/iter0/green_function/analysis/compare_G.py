from viscojapan.plots import plt, MapPlotDisplacement, MapPlotFault, MyBasemap
import viscojapan as vj

fno = 100
scale = 3e-3
epoch = 1200
U = 1e-6
label='%.1G'%U

bm = MyBasemap(
    region_code = 'near',
    )

G_rake95 = vj.EpochalSitesFileReader('../G0_He50km_VisM6.3E18_Rake83.h5')
G_rake90 = vj.EpochalSitesFileReader('../G2_He60km_VisM6.3E18_Rake83.h5')

d0_rake95 = G_rake95.get_epoch_value(0)[:,fno]
d_rake95 = G_rake95.get_epoch_value(epoch)[:,fno]

d0_rake90 = G_rake90.get_epoch_value(0)[:,fno]
d_rake90 = G_rake90.get_epoch_value(epoch)[:,fno]

mplt = MapPlotDisplacement(basemap = bm)
mplt.plot_disp(d_rake90 - d0_rake90, G_rake95.all_sites,
               U = U, label = label,
               X=0.1, Y=0.8,
               color='black', scale=scale)

mplt.plot_disp(d_rake95 - d0_rake95, G_rake90.all_sites,
               U = U, label = label,
               X=0.1, Y=0.7,
               color='red', scale=scale)
##mplt.plot_G_file('../G_He45km.h5', epoch, fno, scale=scale)
##mplt.plot_G_file('../G_He55km.h5', epoch, fno,
##                 color='red', scale=scale)

mplt = MapPlotFault('../../fault_model/fault_bott120km.h5', basemap = bm)
mplt.plot_fault(fno)

plt.show()
