from pylab import plt
import viscojapan as vj

slip = vj.inv.ep.EpochSlip.init_from_file('../../slip0/slip0.h5')

vj.slip.plot.plot_slip_and_rate_at_subflt(slip, 2, 10)


plt.show()
