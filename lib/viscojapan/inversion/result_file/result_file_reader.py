from os.path import exists

import h5py
import numpy as np

from ...file_io_base import FileIOBase
from ...fault_model import FaultFileReader

__all__ = ['ResultFileReader']

class ResultFileReader(FileIOBase):
    def __init__(self, file_name, fault_file=None):
        super().__init__(file_name)
        if fault_file is not None:
            reader = FaultFileReader(fault_file)
            self.num_subflt_along_strike = reader.num_subflt_along_strike
            self.num_subflt_along_dip = reader.num_subflt_along_dip
            self.num_subflts = self.num_subflt_along_strike * self.num_subflt_along_dip
            self.LLons_mid = reader.LLons_mid
            self.LLats_mid = reader.LLats_mid


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
        return [site.decode() for site in m]

    @property
    def num_sites(self):
        return int(len(self.sites))

    @property
    def num_nlin_pars(self):
        return int(self.fid['num_nlin_pars'][...])

    @property
    def incr_slip(self):
        if 'num_nlin_pars' not in self.fid:
            return self.Bm
        else:
            num_nlin_pars = self.num_nlin_pars
            return self.Bm[:-num_nlin_pars]

    @property
    def epochs(self):
        return [int(ii) for ii in self.fid['epochs'][...]]

    @property
    def num_epochs(self):
        return len(self.epochs)

    @property
    def residual_norm_weighted(self):
        return self.fid['misfit/norm_weighted'][...]

    def get_nlin_par_val(self, pn):
        return self.fid['nlin_pars/%s'%pn][...]        

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

    def get_3d_incr_slip(self):
        nx = self.num_subflt_along_strike
        ny = self.num_subflt_along_dip

        slip = self.incr_slip
        slip = slip.reshape([self.num_epochs, ny, nx])

        return slip

    def get_3d_total_slip(self):
        incr_slip = self.get_3d_incr_slip()
        slip = [incr_slip[0,:,:]]
        for ii in incr_slip:
            slip.append(slip[-1]+ii)
        slip = np.asarray(slip)
        return slip

    def get_after_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>0
        assert nth < len(self.epochs)
        
        num_subflts = self.num_subflts
        sslip = self.incr_slip[num_subflts:num_subflts*(nth+1)].reshape([nth, num_subflts])
        slip = sslip.sum(axis=0).reshape([-1,1])
        return slip

    def get_3d_disp(self):
        return self.d_pred.reshape([self.num_epochs, self.num_sites, 3])        
       
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

    def get_post_disp_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        disp = self.get_3d_disp()
        disp_nth = disp[nth,:,:] - disp[0,:,:]
        return disp_nth.reshape([-1,1])

    def get_post_disp_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_post_disp_at_nth_epoch(idx)

    def get_pred_time_series(self,site, cmpt):
        disp = self.get_3d_disp()
        index = self.sites.index(site)
        if cmpt == 'e':
            ts = disp[:,index,0]
        elif cmpt == 'n':
            ts = disp[:,index,1]
        elif cmpt == 'u':
            ts = disp[:,index,2]
        else:
            raise ValueError()
        return ts.flatten(), self.epochs
        
        

    
        
