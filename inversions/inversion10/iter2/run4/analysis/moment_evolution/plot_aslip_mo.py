from pylab import plt

import viscojapan as vj


fault_file = '../../../fault_model/fault_bott80km.h5'
earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'
reader = vj.inv.ResultFileReader('../../outs/ncumurough_06_nedge_12.h5',
                                 fault_file)


compute = vj.MomentCalculator(fault_file, earth_file)
epochs = reader.epochs
mos = []
mws = []


for nth, epoch in enumerate(epochs):
    aslip = reader.get_total_slip_at_nth_epoch(nth)
    mo, mw = compute.compute_moment(aslip)
    mos.append(mo)
    mws.append(mw)

fig, ax1 = plt.subplot()
ax1.plot(epochs, mos)

ax2 = ax1.twinx()
ax2.plot(epochs, mws)


##plt.grid('on')
##plt.ylabel('Moment(Nm)')
##
##plt.subplot(212)
##plt.plot(epochs, mws)
##plt.grid('on')
##plt.xlabel('days after the mainshock')
##plt.ylabel('Mw')
plt.savefig('total_slip_mo_mw_evolution.pdf')
plt.show()
plt.close()


##mos = []
##mws = []
##for nth, epoch in enumerate(epochs):
##    if nth == 0:
##        continue
##    aslip = reader.get_after_slip_at_nth_epoch(nth)
##    mo, mw = compute.compute_moment(aslip)
##    mos.append(mo)
##    mws.append(mw)
##
##plt.subplot(211)
##plt.plot(epochs[1:], mos,'-o')
##plt.grid('on')
##plt.ylabel('Moment(Nm)')
##
##plt.subplot(212)
##plt.plot(epochs[1:], mws,'-o')
##plt.grid('on')
##plt.xlabel('days after the mainshock')
##plt.ylabel('Mw')
##
##plt.savefig('after_slip_mo_mw_evolution.pdf')
##plt.close()
