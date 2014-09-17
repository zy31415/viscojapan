import numpy as np
from scipy.interpolate import griddata
import h5py
from pylab import plt

import viscojapan as vj
from epochs_log import epochs

num_epochs = len(epochs)

f_res = '../outs/seasd_01_nrough_10_nedge_05.h5'

with h5py.File(f_res) as fid:
    d_pred = fid['d_pred'][...].reshape((num_epochs, -1,3))

d_co = d_pred[0]

d_mag = np.linalg.norm(d_co, axis=1)

f_sites = '../../sites_with_seafloor'
sites = np.loadtxt(f_sites,'4a')
lons, lats = vj.get_pos(sites)

# define regular grid spatially covering input data
n = 50
xg = np.linspace(lons.min(), lons.max(),n)
yg = np.linspace(lats.min(), lats.max(),n)
X,Y = np.meshgrid(xg,yg)

# interpolate Z values on defined grid
Z = griddata(np.vstack((lons.flatten(),lats.flatten())).T, \
  np.vstack(d_mag.flatten()),(X,Y),method='cubic').reshape(X.shape) 

bm = vj.MyBasemap(region_code='all')
CS = bm.contour(x=X, y=Y, data=Z, N=None, levels=[0.5, 0.1, 0.01, 0.001],latlon=True)
plt.clabel(CS, inline=1, fontsize=10)
plt.show()
