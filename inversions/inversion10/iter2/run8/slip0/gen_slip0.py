import h5py
from pylab import plt

import viscojapan as vj

with h5py.File('nrough_05_naslip_11.h5') as fid:
    incr_slip = fid['Bm'][:-3][...]
    epochs = fid['epochs'][...]

num_epochs = len(epochs)

incr_slip = incr_slip.reshape([num_epochs, 12, 28])

slip = vj.slip.Slip.init_from_incr3d(incr_slip, epochs)

## vj.slip.plot.plot_slip_and_rate_at_subflt(slip, 4, 10)
## plt.show()

with h5py.File('slip0.h5','w') as fid:
    fid['data3d'] = slip.get_cumu_slip_3d
    fid['epochs'] = epochs
