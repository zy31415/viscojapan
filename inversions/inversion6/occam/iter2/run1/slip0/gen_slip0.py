import h5py

import viscojapan as vj

from epochs import epochs

with h5py.File('co_ndamp_00_rough_06.h5','r') as fid:
    co_slip = fid['Bm'][...]

num_subfaults = len(co_slip)

with h5py.File('afterslip_nrough_09.h5','r') as fid:
    slip = fid['Bm'][...][:-3]

ep = vj.EpochalData('incr_slip0.h5')
ep[0] = co_slip

for nth, epoch in enumerate(epochs[1:]):
    ep[epoch] = slip[nth*num_subfaults:
                     (nth+1)*num_subfaults]
assert (nth+1)*num_subfaults == len(slip)

