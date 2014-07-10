from viscojapan.plots import MapPlotDisplacement, plt
from viscojapan.plots import MapPlotFault


fno = 325

mplt = MapPlotDisplacement()
mplt.plot_G_file(f_G='../G.h5', epoch=0, mth=fno)

mplt = MapPlotFault('../fault_He50km.h5')
mplt.plot_fault(fno=fno)

plt.show()
