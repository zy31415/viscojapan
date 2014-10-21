import h5py

import viscojapan as vj

from epochs_log import epochs

with h5py.File('outs/ano_11_bno_10.h5','r') as fid:
    Bm = fid['Bm'][...]

vj.break_col_vec_into_epoch_file(Bm, epochs, 'incr_slip0.h5')

