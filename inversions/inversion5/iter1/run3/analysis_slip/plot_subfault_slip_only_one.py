import h5py
import numpy as np
from pylab import plt

from epochs_log import epochs

with h5py.File('../outs/seasd_01_nrough_10_nedge_05.h5') as fid:
    Bm = fid['Bm']
    incr_slip = Bm[:-3]
    incr_slip = incr_slip.reshape([21,10, 35])

slip = [incr_slip[0,:,:]]
for ii in incr_slip:
    slip.append(slip[-1]+ii)
slip = np.asarray(slip)

ii = 3
jj = 15
slip_subflt = slip[:,ii,jj][0:-1]

plt.fill_between(x=epochs, y1=slip_subflt, y2=0, color='r')
plt.gca().set_xscale('log')
plt.xlim([0.9, 1200])
plt.ylim([0,100])
plt.grid('on')
plt.box('on')
plt.ylabel('slip/m')
plt.xlabel('day')
plt.savefig('slip_on_one_subflt.png')
plt.show()


