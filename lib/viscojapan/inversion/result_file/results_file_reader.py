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
    def log10_He_(self):
        return self.fid['nlin_pars/log10(He)'][...]

    @property
    def log10_visM_(self):
        return self.fid['nlin_pars/log10(visM)'][...]

    @property
    def rake(self):
        return self.fid['nlin_pars/rake'][...]

    @property
    def roughening_norm(self):
        return self.fid['regularization/roughening/norm'][...]

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
    def num_sites(self):
        return int(self.fid['num_sites'][...])

    @property
    def num_nlin_pars(self):
        return self.fid['num_nlin_pars'][...]

    @property
    def incr_slip(self):
        if 'num_nlin_pars' not in self.fid:
            return self.Bm
        else:
            num_nlin_pars = self.num_nlin_pars
            return self.Bm[:-num_nlin_pars]

    @property
    def epochs(self):
        return list(self.fid['epochs'][...])

    @property
    def num_epochs(self):
        return self.fid['num_epochs'][...]

    @property
    def num_subflts(self):
        return int(self.fid['num_subflts'][...])

    @property
    def residual_norm_weighted(self):
        return self.fid['misfit/norm_weighted'][...]

    def get_incr_slip_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_incr_slip_at_nth_epoch(idx)

    def get_incr_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        num_subflts = self.num_subflts
        return self.incr_slip[num_subflts*nth:num_subflts*(nth+1)]

    def get_total_slip_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_total_slip_at_nth_epoch(idx)

    def get_total_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        num_subflts = self.num_subflts
        sslip = self.incr_slip[:num_subflts*(nth+1)].reshape([nth+1, num_subflts])
        slip = sslip.sum(axis=0).reshape([-1,1])
        return slip

    def get_after_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>0
        assert nth < len(self.epochs)
        
        num_subflts = self.num_subflts
        sslip = self.incr_slip[num_subflts:num_subflts*(nth+1)].reshape([nth, num_subflts])
        slip = sslip.sum(axis=0).reshape([-1,1])
        return slip
       
    def get_disp_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        num_sites = self.num_sites
        return self.d_pred[num_sites*3*nth:num_sites*3*(nth+1)]

    def get_disp_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_disp_at_nth_epoch(idx)
        
        

    
        
