from os.path import exists

import h5py
import numpy as np

from ...file_io_base import FileIOBase
from ...fault_model import FaultFileReader
from ...moment import ComputeMoment
from ...plots import plot_Mos_Mws

__all__ = ['ResultFileReader']

class ResultFileReader(FileIOBase):
    def __init__(self, file_name, fault_file=None, earth_file=None):
        super().__init__(file_name)
        if fault_file is not None:
            reader = FaultFileReader(fault_file)
            self.num_subflt_along_strike = reader.num_subflt_along_strike
            self.num_subflt_along_dip = reader.num_subflt_along_dip
            self.num_subflts = self.num_subflt_along_strike * self.num_subflt_along_dip
            self.LLons_mid = reader.LLons_mid
            self.LLats_mid = reader.LLats_mid
            self.fault_file = fault_file

        self.earth_file = earth_file


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
    def d_obs(self):
        m = self.fid['d_obs'][...]
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
            if num_nlin_pars ==0:
                return self.Bm
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

    @property
    def rms(self):
        return float(self.fid['misfit/rms'][...])

    @property
    def rms_inland(self):
        return float(self.fid['misfit/rms_inland'][...])

    @property
    def rms_inland_at_epoch(self):
        return self.fid['misfit/rms_inland_at_epoch'][...]

    def get_rms_at_sites(self,cmpt):
        return self.fid['misfit/at_sites/%s'%cmpt][...]   

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
        assert nth>=0
        assert nth < len(self.epochs)

        num_subflts = self.num_subflts
        
        if nth > 0:
            sslip = self.incr_slip[num_subflts:num_subflts*(nth+1)].reshape([nth, num_subflts])
            slip = sslip.sum(axis=0).reshape([-1,1])
        if nth == 0:
            slip = np.zeros((num_subflts,1))
        return slip

    def get_total_slip_Mos_Mws(self):
        assert self.earth_file is not None, 'Missing earth_file!'
        compute = ComputeMoment(self.fault_file, self.earth_file)
        epochs = self.epochs
        mos = []
        mws = []
        for nth, epoch in enumerate(epochs):
            aslip = self.get_total_slip_at_nth_epoch(nth)
            mo, mw = compute.compute_moment(aslip)
            mos.append(mo)
            mws.append(mw)
        return mos, mws, epochs

    def get_afterslip_Mos_Mws(self):
        assert self.earth_file is not None, 'Missing earth_file!'
        compute = ComputeMoment(self.fault_file, self.earth_file)
        epochs = self.epochs
        mos = []
        mws = []
        _epochs = []
        for nth, epoch in enumerate(epochs):
            if epoch == 0:
                continue
            aslip = self.get_after_slip_at_nth_epoch(nth)
            mo, mw = compute.compute_moment(aslip)
            mos.append(mo)
            mws.append(mw)
            _epochs.append(epoch)
        return mos, mws, _epochs

    def plot_total_slip_Mos_Mws(self,
                                ylim = None,
                                yticks = None,
                                ):
        assert self.earth_file is not None, 'Missing earth_file!'
        mos, mws, epochs = self.get_total_slip_Mos_Mws()
        plot_Mos_Mws(epochs, Mos = mos, ylim=ylim, yticks=yticks)
        

    def plot_afterslip_Mos_Mws(self,
                               ylim = None,
                               yticks = None,):
        assert self.earth_file is not None, 'Missing earth_file!'
        mos, mws, epochs = self.get_afterslip_Mos_Mws()
        plot_Mos_Mws(epochs[1:], Mos = mos[1:], ylim=ylim, yticks=yticks)

    
        
