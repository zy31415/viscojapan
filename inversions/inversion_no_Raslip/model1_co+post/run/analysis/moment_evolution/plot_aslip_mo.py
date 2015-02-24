import numpy as np
from pylab import plt

import viscojapan as vj


fault_file = '../../../fault_model/fault_bott80km.h5'
earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'
reader = vj.inv.ResultFileReader('../../outs/nrough_06_naslip_11.h5')

slip = reader.get_slip()

cal = vj.moment.MomentCalculator(fault_file, earth_file)

mos, mws = cal.get_afterslip_Mos_Mws(slip)
epochs = slip.get_epochs()

vj.moment.plot_Mos_Mws(epochs,
                       mos,
                       ylim=(1e21, 10.2e21),
                       yticks = (2e21, 4e21, 6e21, 8e21, 10e21)
)

plt.savefig('after_slip_mo_mw_evolution.pdf')
plt.show()
plt.close()

mos, mws = cal.get_cumu_slip_Mos_Mws(slip)
epochs = slip.get_epochs()

vj.moment.plot_Mos_Mws(epochs,
                       mos,
                       ylim = (7.1e22, 8.4e22),
                       yticks = [7.2e22, 7.4e22, 7.6e22, 7.8e22, 8.0e22, 8.2e22, 8.4e22]
)
plt.savefig('cumu_slip_mo_mw_evolution.pdf')
plt.show()
plt.close()
