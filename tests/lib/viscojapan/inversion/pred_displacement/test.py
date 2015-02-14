import h5py
import numpy as np

import viscojapan as vj

file_G0 = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5'

with h5py.File(file_G0) as fid:
    g = vj.epoch_3d_array.EpochSites3DArray.load(fid,memory_mode=False)

    
    arr = g._array_3d
    print(type(arr))
    
    mask1 = range(28)
    mask2 = np.asarray([True]*28)
    for n in range(30):
        arr[mask1,:,:]
