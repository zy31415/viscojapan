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
print(mos, mws)
plt.plot(epochs[1:], mos, label='only afterslip without seafloor')

####################
mos = []
mws = []

for epoch in epochs[1:]:
    reader = vj.inv.ResultFileReader('../../run2/outs/outs_%04d/naslip_%02d.h5'%(epoch,10))
    s = reader.m
    mo, mw = cal.compute_moment(s)
    mos.append(mo)
    mws.append(mw)
print(mos, mws)
plt.plot(epochs[1:], mos, '-x',label='only afterslip with seafloor')



plt.legend(loc=0)
plt.savefig('Maslip.png')
plt.show()
