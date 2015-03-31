import numpy as np
from pylab import plt

import viscojapan as vj


fault_file = '../../../fault_model/fault_bott80km.h5'
earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'

##
reader = vj.inv.ResultFileReader('../../outs/nrough_06_naslip_11.h5')
slip = reader.get_slip()
cal = vj.moment.MomentCalculator(fault_file, earth_file)
mos, mws = cal.get_afterslip_Mos_Mws(slip)
print(mos, mws)

epochs = slip.get_epochs()
vj.moment.plot_Mos_Mws(epochs, Mos = mos,
                       ylim=[1e21,1.3e22],
                       yticks = [0.2e22, 0.4e22,0.6e22,.8e22,1e22, 1.2e22]
                       )
plt.savefig('mos_mws_nrough_06_naslip_11.pdf')
plt.show()
plt.close()


##
reader = vj.inv.ResultFileReader('../../outs/nrough_06_naslip_10.h5')
slip = reader.get_slip()
cal = vj.moment.MomentCalculator(fault_file, earth_file)
mos, mws = cal.get_afterslip_Mos_Mws(slip)
epochs = slip.get_epochs()
vj.moment.plot_Mos_Mws(epochs, Mos = mos,
                       ylim=[1e21,1.3e22],
                       yticks = [0.2e22, 0.4e22,0.6e22,.8e22,1e22, 1.2e22]
                       )

plt.savefig('mos_mws_nrough_06_naslip_10.pdf')
plt.show()
plt.close()
