__author__ = 'zy'

import viscojapan as vj

reader = vj.inv.DeformPartitionResultReader('share/deform_partition.h5')

Ecumu = reader.Ecumu
Rco = reader.Rco
Raslip = reader.Raslip


site = vj.SitesDB().get('_MGW')

y_Ecumu = Ecumu.cumu_ts(site,'e')
y_Rco = Rco.cumu_ts(site,'e')
y_Raslip = Raslip.cumu_ts(site,'e')
epochs = Ecumu.epochs


y_added = y_Ecumu + y_Rco + y_Raslip


reader = vj.inv.ResultFileReader('share/nrough_05_naslip_11.h5')
sites = reader.sites
pred_disp = reader.get_pred_disp()
y_pred = pred_disp.cumu_ts(site, 'e')

from pylab import plt

plt.plot(epochs, y_added,'x')
plt.plot(epochs, y_pred, '.')
plt.show()
