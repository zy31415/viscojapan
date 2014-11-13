from ..fault_model import FaultFileReader

import h5py
import numpy as np

__all__ = ['get_slip_results_for_gmt']

def get_middle_point(x):
    x1 = (x[:-1,:] + x[1:,:])/2.
    x2 = (x1[:,:-1] + x1[:,1:])/2.
    return x2

def get_slip_results_for_gmt(res_file, fault_file):        
    reader = FaultFileReader(fault_file)
    lats = reader.LLats
    lons = reader.LLons

    lats_m = get_middle_point(lats)
    lons_m = get_middle_point(lons)

    with h5py.File(res_file) as fid:
        Bm = fid['Bm'][...]

    slip = Bm.reshape([-1, reader.num_subflt_along_strike])

    _arr = np.array([lons_m.flatten(), lats_m.flatten(), slip.flatten()]).T

    return _arr
