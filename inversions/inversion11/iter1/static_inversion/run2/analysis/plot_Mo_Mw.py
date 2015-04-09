import numpy as np
from pylab import plt

import viscojapan as vj

from epochs import epochs

fault_file = '../../../fault_model/fault_bott80km.h5'

earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'

cal = vj.mo.MomentCalculator(fault_file, earth_file)

mos = []
mws = []

for epoch in epochs[1:]:
    reader = vj.inv.ResultFileReader('../outs/outs_%04d/naslip_%02d.h5'%(epoch,10))
    s = reader.m
    mo, mw = cal.compute_moment(s)
    mos.append(mo)
    mws.append(mw)

plt.plot(epochs[1:], mos, label='only afterslip')

########################
reader = vj.inv.ResultFileReader('../../../run11/outs/nrough_06_naslip_11.h5')
slip = reader.get_slip()
epochs = slip.get_epochs()
mos1, mws1 = cal.get_afterslip_Mos_Mws(slip)
print(mos1, mws1)
plt.plot(epochs, mos1, 'x-', label='coupled model')

################################
reader = vj.inv.ResultFileReader('../../../../../inversion_no_Raslip/model1_co+post/model1/run3/outs/nrough_06_naslip_11.h5')
slip = reader.get_slip()
epochs = slip.get_epochs()
mos1, mws1 = cal.get_afterslip_Mos_Mws(slip)

plt.plot(epochs, mos1, '^-', label='no Raslip model')

plt.legend(loc=0)
plt.savefig('Maslip.png')
plt.show()
