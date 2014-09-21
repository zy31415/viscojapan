import h5py
import numpy as np

##with h5py.File('fault_bott50km_point_source.h5') as fid:
##    del fid['x_f']
##    del fid['y_f']
    
with h5py.File('fault_bott50km_point_source.h5') as fid:
    fid['x_f'] = np.arange(0,721,20)    
    fid['y_f'] = np.arange(0,241,20)
