from pylab import plt

import viscojapan as vj

reader = vj.ResultFileReader('../outs/nrough_06.h5')
fault_file = '../../fault_model/fault_bott60km.h5'
earth_file = '../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'

compute = vj.MomentCalculator(fault_file, earth_file)
epochs = reader.epochs
mos = []
mws = []


for nth, epoch in enumerate(epochs):
    aslip = reader.get_total_slip_at_nth_epoch(nth)
    mo, mw = compute.compute_moment(aslip)
    mos.append(mo)
    mws.append(mw)

plt.subplot(211)
plt.plot(epochs, mos)
plt.subplot(212)
plt.plot(epochs, mws)
plt.savefig('total_slip_mo_mw_evolution.png')
plt.close()


mos = []
mws = []
for nth, epoch in enumerate(epochs):
    if nth == 0:
        continue
    aslip = reader.get_after_slip_at_nth_epoch(nth)
    mo, mw = compute.compute_moment(aslip)
    mos.append(mo)
    mws.append(mw)

plt.subplot(211)
plt.plot(epochs[1:], mos)
plt.subplot(212)
plt.plot(epochs[1:], mws)
plt.savefig('after_slip_mo_mw_evolution.png')
plt.close()
