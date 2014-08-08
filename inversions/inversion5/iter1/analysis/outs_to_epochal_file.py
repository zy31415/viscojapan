import glob
from os.path import join, basename
import sys

import h5py
import numpy as np

import viscojapan as vj

sys.path.append('../')
from epochs_log import epochs


sites = np.loadtxt('../sites_with_seafloor','4a')

files = glob.glob('../outs/ano_??_bno_10.h5')

for file in files:
    of = join('outs_epochal_pred_disp/',basename(file))
    with h5py.File(file) as fid:
        d_pred = fid['d_pred']
        info_dic = {
            'sites' : sites
            }
        vj.break_col_vec_into_epoch_file(d_pred, epochs, of)
