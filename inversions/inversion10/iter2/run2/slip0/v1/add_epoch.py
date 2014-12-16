import h5py
import numpy as np

with h5py.File('slip0.h5') as fid:
    arr = fid['epochs/0000'][...]
    fid['epochs/1800'] = np.zeros_like(arr)
