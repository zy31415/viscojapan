import h5py
import numpy as np
from pylab import plt

with h5py.File('outs/nrough_00.h5') as fid:
    nlin_corr = fid['nlin_correction'][...]
    corr_vis = nlin_corr[:,0].reshape([-1,3])
    corr_He = nlin_corr[:,1].reshape([-1,3])
    corr_rake = nlin_corr[:,2].reshape([-1,3])
    corr_total = corr_vis + corr_He + corr_rake
    d_pred = fid['d_pred'][...].reshape([-1,3])


norm_corr_vis = np.linalg.norm(corr_vis, axis=1)
norm_corr_He = np.linalg.norm(corr_He, axis=1)
norm_corr_rake = np.linalg.norm(corr_rake, axis=1)

norm_corr_total = np.linalg.norm(corr_total, axis=1)

norm_d_pred = np.linalg.norm(d_pred, axis=1)

percentage = abs(norm_corr_total)/abs(norm_d_pred)

plt.hist(percentage, range=(0,1), bins=40)
plt.show()
