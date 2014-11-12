from os.path import join

import h5py
import numpy as np

import viscojapan as vj
import pGMT

def get_middle_point(x):
    x1 = (x[:-1,:] + x[1:,:])/2.
    x2 = (x1[:,:-1] + x1[:,1:])/2.
    return x2

base_dir = '/home/zy/workspace/viscojapan/inversions/static_inversion/static_inversion2'
res_file = join(
    base_dir,
    'coseismic/run1_seafloor_inf/outs/nrough_10_ntop_00.h5')
fault_file = join(
    base_dir,
    'fault_model/fault_bott60km.h5')

reader = vj.FaultFileReader(fault_file)
lats = reader.LLats
lons = reader.LLons

lats_m = get_middle_point(lats)
lons_m = get_middle_point(lons)

with h5py.File(res_file) as fid:
    Bm = fid['Bm'][...]

slip = Bm.reshape([-1, reader.num_subflt_along_strike])

_arr = np.array([lons_m.flatten(), lats_m.flatten(), slip.flatten()]).T
np.savetxt('coseismic_slip.txt', _arr, "%f %f %f")
