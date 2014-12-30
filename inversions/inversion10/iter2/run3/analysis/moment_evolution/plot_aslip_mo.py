import numpy as np
from pylab import plt

import viscojapan as vj


fault_file = '../../../fault_model/fault_bott80km.h5'
earth_file = '../../../earth_model_nongravity/He50km_VisM6.3E18/earth.model_He50km_VisM6.3E18'
reader = vj.inv.ResultFileReader('../../outs/nrough_05_naslip_11.h5',
                                 fault_file, earth_file)

reader.plot_total_slip_Mos_Mws(
    ylim=(6.9e22, 8.1e22),
    yticks = [7e22, 7.2e22, 7.4e22, 7.6e22, 7.8e22, 8.0e22, ]
    )
plt.savefig('total_slip_mo_mw_evolution.pdf')
plt.show()
plt.close()

##
reader.plot_afterslip_Mos_Mws(
    ylim=(2.5e21, 10.2e21),
    yticks = (3e21, 4e21, 5e21, 6e21, 7e21, 8e21, 9e21, 10e21)
    )
plt.savefig('after_slip_mo_mw_evolution.pdf')
plt.show()
plt.close()
