import glob

import h5py

files = glob.glob('outs/bno_??_cno_??.h5')

for file in files:
    with h5py.File(file,'r') as fid:
        nres = fid['residual_norm_weighted'][...]
##        if nres < 13:
##            print(file)
        if nres < 14 and nres >= 13:
            print(file)
