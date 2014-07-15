from viscojapan.fault_model.fault_file_io import FaultFileIO
from viscojapan.plots import MapPlotFault, plt, MapPlotSlab

mplt = MapPlotFault('fault_He50km_1.h5')
mplt.plot_fault()

mplt = MapPlotFault('fault_He50km_2.h5')
mplt.plot_fault(color='red')

MapPlotSlab().plot_top()

plt.show()
