import numpy as np
from pylab import plt

from viscojapan.epochal_data import EpochalG

fno = 30
scale = .0005
epoch = 1200
U = 1e-6
label='%.1G'%U

sites = np.loadtxt('sites_without_seafloor','4a,', usecols=(0,))

G45km = EpochalG('../G_He45km.h5', filter_sites=sites)
G50km = EpochalG('../G_He50km.h5', filter_sites=sites)
G55km = EpochalG('../G_He55km.h5', filter_sites=sites)

d0_45km = G45km.get_epoch_value(0)[:,fno]
d_45km = G45km.get_epoch_value(epoch)[:,fno] - d0_45km 

d0_50km = G50km.get_epoch_value(0)[:,fno]
d_50km = G50km.get_epoch_value(epoch)[:,fno] - d0_50km

d0_55km = G55km.get_epoch_value(0)[:,fno]
d_55km = G55km.get_epoch_value(epoch)[:,fno] - d0_55km


dd = d_55km-d_50km
y1 = dd/np.log10(55/50)
y1 = dd/5

dd = d_50km-d_45km
y2 = dd/np.log10(50/45)
y2 = dd/5

dd = d_55km-d_45km
y3 = dd/np.log10(55/45)
y3 = dd/10

plt.hist(y1, 100, range=(-1e-6, 1e-6))
plt.hist(y2, 100, range=(-1e-6, 1e-6))
plt.hist(y3, 100, range=(-1e-6, 1e-6))
plt.show()
