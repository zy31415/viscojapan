import numpy as np
from pylab import plt

import viscojapan as vj

tp = np.loadtxt('ozawa_2011_obs_file','4a,3f')
sites = [ii[0] for ii in tp]
disp0 = np.asarray([ii[1] for ii in tp]).flatten()
e0 = disp0[0::3]
n0 = disp0[1::3]
u0 = disp0[2::3]

ep = vj.EpochalDisplacement('cumu_post_with_seafloor.h5',
                            filter_sites=sites)
disp1 = ep[0].flatten()
e1 = disp1[0::3]
n1 = disp1[1::3]
u1 = disp1[2::3]

h_diff = np.sqrt((e0-e1)**2 + (n0-n1)**2) / np.sqrt(e0**2 + n0**2)
v_diff = np.abs(u0-u1) / np.abs(u0)

#plt.hist(h_diff, bins=20)
plt.hist(v_diff[~np.isinf(v_diff)], bins=10, range=(1,200))
plt.xlabel("Relative difference between mine and Ozawa's with respec to Ozawa's")
plt.ylabel('No. of stations')
plt.grid('on')
plt.savefig('error.pdf')
#plt.xlim([0,1])
plt.show()

vj.
