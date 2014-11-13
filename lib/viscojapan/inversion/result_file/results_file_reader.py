from os.path import exists

import h5py
import numpy as np

from ...fault_model import FaultFileReader
from ...file_io_base import FileIOBase

__all__ = ['get_slip_results_for_gmt','ResultFileReader']

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

class ResultFileReader(FileIOBase):
    def __init__(self, file_name):
        super().__init__(file_name)        

    def open(self):
        assert exists(self.file_name)
        return h5py.File(self.file_name,'r')

    @property
    def Bm(self):
        Bm = self.fid['Bm'][...]
        return Bm

    @property
    def m(self):
        m = self.fid['m'][...]
        return m

    @property
    def num_nlin_pars(self):
        return self.fid['num_nlin_pars'][...]

    @property
    def slip(self):
        if 'num_nlin_par' not in fid:
            return self.Bm
        else:
            num_nlin_pars = self.num_nlin_pars
            return self.Bm[:-num_nlin_pars]

    
        
