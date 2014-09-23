import pickle

import h5py
import numpy as np
from pylab import plt

import viscojapan as vj

from epochs import epochs

f_res = '../outs/nrough_10.h5'

sites = np.loadtxt('../sites','4a,')
num_sites = len(sites)
num_obs = 3*len(sites)
num_epochs = len(epochs)

with h5py.File(f_res,'r') as fid:
    d_pred = fid['d_pred'][...]
d_pred = d_pred.reshape([num_epochs, num_sites, 3])

ep = vj.EpochalDisplacement('../../../cumu_post_with_seafloor.h5','../../sites_with_seafloor')
d = ep.vstack(epochs)
d = d.reshape([num_epochs, num_sites,3])


ch = vj.choose_inland_GPS(sites)

misfit_inland = d_pred[:,ch,:]-d[:,ch,:]

rmses = []
for mi in misfit_inland:
    print(mi.shape)
    rms = np.sqrt(np.mean(mi.flatten()**2))
    rmses.append(rms)
rms_total = np.linalg.norm(misfit_inland.flatten())

#plt.semilogx(epochs, rmses,'o-')

with open('rms_deconv.pkl','wb') as fid:
    pickle.dump((epochs, rmses), fid)

plt.plot(epochs, rmses,'o-')
#plt.axhline(rms_total)
plt.grid('on')
plt.xlabel('days after mainshock')
plt.ylabel('RMS(m)')
plt.xlim([-50,1200])
plt.show()
##    
