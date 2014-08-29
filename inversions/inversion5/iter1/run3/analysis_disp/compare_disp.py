import h5py
import numpy as np
from pylab import plt

import viscojapan as vj

from epochs_log import epochs

f_res = '../outs/seasd_01_nrough_10_nedge_05.h5'

sites =np.loadtxt('../../sites_with_seafloor','4a,')
num_obs = len(sites)*3
num_epochs = len(epochs)

with h5py.File(f_res,'r') as fid:
    d_pred = fid['d_pred'][...]

d_pred = d_pred.reshape([num_epochs, num_obs])

site = b'J587'
idx = list(sites).index(site)

y_pred_e = d_pred[:,idx*3]
y_pred_n = d_pred[:,idx*3+1]
y_pred_u = d_pred[:,idx*3+2]
y_preds = [y_pred_e, y_pred_n, y_pred_u]

tp = np.loadtxt('/home/zy/workspace/viscojapan/tsana/post_fit/cumu_post_displacement/%s.cumu'\
                %(site.decode()))
t = tp[:,0]
y_obs_e = tp[:,1]
y_obs_n = tp[:,2]
y_obs_u = tp[:,3]
y_obses = [y_obs_e, y_obs_n, y_obs_u]

##plt.semilogx(t, ts_e_obs - ts_e_obs[0],'x-')
##plt.semilogx(epochs, ts_e - ts_e[0],'o-')

fig, axes = plt.subplots(3,1,sharex=True)
for ax, y_obs, y_pred in zip(axes, y_obses, y_preds):
    fig.sca(ax)
    plt.plot(t, y_obs,'-')
    plt.plot(epochs, y_pred,'o-')
    plt.grid('on')
fig.subplots_adjust(hspace=0.1)
fig.suptitle(site.decode())
plt.show()
