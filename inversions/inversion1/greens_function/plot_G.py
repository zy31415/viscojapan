from viscojapan.plots import MapPlotDisplacement, plt, MapPlotFault

fno = 384
mplt = MapPlotDisplacement()
mplt.plot_G_file('G.h5',1200,fno)

mplt = MapPlotFault('../fault_model/fault_He50km_east.h5')
mplt.plot_fault(fno= fno)

plt.show()
