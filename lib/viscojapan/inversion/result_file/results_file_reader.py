from os.path import exists

import h5py
import numpy as np

from ...fault_model import FaultFileReader
from ...file_io_base import FileIOBase

__all__ = ['ResultFileReader']

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
    def d_pred(self):
        m = self.fid['d_pred'][...]
        return m
    @property
    def sites(self):
        m = self.fid['sites'][...]
        return m 

    @property
    def num_nlin_pars(self):
        return self.fid['num_nlin_pars'][...]

    @property
    def slip(self):
        if 'num_nlin_par' not in self.fid:
            return self.Bm
        else:
            num_nlin_pars = self.num_nlin_pars
            return self.Bm[:-num_nlin_pars]

    
        
