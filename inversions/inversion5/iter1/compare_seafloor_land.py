import glob

import h5py

import viscojapan as vj
from epochs_log import epochs

files = glob.glob('outs/ano_??_bno_10.h5')

for file in files:
    with h5py.File(file) as fid:
        d_pred = fid['d_pred'][...]
        vj.break_col_vec_into_epoch_file(
        vj.break_col_vec_into_epoch_file(d_pred, epochs, fn)
