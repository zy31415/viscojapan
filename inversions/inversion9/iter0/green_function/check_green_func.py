import viscojapan as vj
from pylab import plt

reader = vj.EpochalFileReader('G0_He50km_VisM6.3E18_Rake83.h5')

fno = 430 - 35 - 35 - 35
day = 1200
disp0 = reader[0][:,fno]
disp = reader[day][:,fno] - disp0

##tp = reader['sites']
##sites = [ii[0] for ii in tp]

sites = reader['sites']

scale = 0.02

mplt = vj.plots.MapPlotDisplacement()
mplt.plot_disp(disp,sites, scale=scale,
               U=2e-3,
               Y=0.8,
               label = '2e-3')

mplt = vj.plots.MapPlotFault('../fault_model/fault_bott60km.h5')
mplt.plot_fault(fno = fno)

plt.show()
