import h5py
import numpy as np
from pylab import plt

import viscojapan as vj

from epochs_log import epochs

f_res = '../outs/seasd_01_nrough_10_nedge_05.h5'

sites = np.loadtxt('../../sites_with_seafloor','4a,')
num_obs = 3*len(sites)

with h5py.File(f_res,'r') as fid:
    d_pred = fid['d_pred'][...]
d_pred = d_pred.reshape([num_obs,-1])

ep = vj.EpochalDisplacement('../../../cumu_post_with_seafloor.h5','../../sites_with_seafloor')
d = ep.vstack(epochs)
d = d.reshape([num_obs,-1])

def choose_inland_GPS(sites):
    ch = []
    for site in sites:
        if site.decode()[0]=='_':
            ch.append(False)
        else:
            ch.append(True)
    return np.asarray(ch,bool)

ch = choose_inland_GPS(sites)

misfit_inland = d_pred[ch,:]-d[ch,:]

rmses = []
for mi in misfit_inland.T:
    rms = np.linalg.norm(mi)
    rmses.append(rms)

rms_total = np.linalg.norm(misfit_inland.flatten())

plt.semilogx(epochs, rmses,'o-')
plt.axhline(rms_total)
plt.grid('on')
plt.show()
    
