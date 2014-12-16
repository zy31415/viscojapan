from pylab import plt

import viscojapan as vj

fault_file = '../../../fault_model/fault_bott80km.h5'

reader = vj.inv.ResultFileReader('../../outs/nrough_06_naslip_10.h5',
                                 fault_file)
co_slip = reader.get_incr_slip_at_nth_epoch(0)
aslip = reader.get_after_slip_at_nth_epoch(2)



mplt = vj.plots.MapPlotFault(fault_file)
#mplt.plot_slip(co_slip)
mplt.plot_slip(aslip)
mplt.plot_fault()

mplt = vj.plots.MapPlotSlab()
mplt.plot_top()
mplt.plot_dep_contour(dep=-80, color='red')
mplt.plot_dep_contour(dep=-60, color='red')
plt.show()
