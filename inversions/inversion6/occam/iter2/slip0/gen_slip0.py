import h5py

import viscojapan as vj

from epochs_log import epochs

with h5py.File('coseismic_slip_nrough_07_ndamp_06.h5','r') as fid:
    Bm0 = fid['Bm'][...]

with h5py.File('ano_08_bno_07.h5','r') as fid:
    Bm1 = fid['Bm'][...]

num_subflts = len(Bm0)
Bm1[:num_subflts,:]=Bm0

vj.break_col_vec_into_epoch_file(Bm1, epochs, 'incr_slip0.h5')

