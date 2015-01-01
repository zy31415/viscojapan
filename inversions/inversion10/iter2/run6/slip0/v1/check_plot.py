import viscojapan as vj
from pylab import plt

nth_epoch = 28
fault_file = '../../../fault_model/fault_bott80km.h5'

reader = vj.EpochalFileReader('slip0.h5')
epochs = reader.get_epochs()
slip = reader[epochs[nth_epoch]]
plt.subplot(1,2,1)
mplt = vj.plots.MapPlotFault(fault_file)
mplt.plot_slip(slip)

#############
fault_file = '../../../../iter0/fault_model/fault_bott120km.h5'
reader = vj.inv.ResultFileReader('nco_06_naslip_10.h5',fault_file)
slip = reader.get_incr_slip_at_nth_epoch(nth_epoch)

plt.subplot(1,2,2)
mplt = vj.plots.MapPlotFault(fault_file)
mplt.plot_slip(slip)
plt.show()

plt.close()

