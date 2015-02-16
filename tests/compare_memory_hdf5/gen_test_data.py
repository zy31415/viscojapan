import numpy as np
import h5py


with h5py.File('test_data.h5','w') as fid:
    fid['data'] = np.zeros([100,1000,100])

