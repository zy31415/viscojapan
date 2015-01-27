import h5py
import numpy as np
from pylab import plt

import viscojapan as vj
from epochs_log import epochs

with h5py.File('../outs/seasd_01_nrough_10_nedge_05.h5') as fid:
    Bm = fid['Bm']
    incr_slip = Bm[:-3]
    incr_slip = incr_slip.reshape([21,10, 35])

slip = [incr_slip[0,:,:]]
for ii in incr_slip:
    slip.append(slip[-1]+ii)
slip = np.asarray(slip)

cm = vj.MomentCalculator('../../fault_model/fault_bott40km.h5',
                 'earth.modelBURG-SUM_40km')
mo = []
mw = []
for s in slip:
    m1, m2 = cm.moment(s)
    mo.append(m1)
    mw.append(m2)

plt.semilogx(epochs, mw[:-1])
plt.show()
