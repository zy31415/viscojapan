import numpy as np

from .result_file_reader import ResultFileReader
from ...fault_model import FaultFileReader
from ...moment import MomentCalculator, plot_Mos_Mws

__all__ = ['SlipResultReader']

class SlipResultReader(ResultFileReader):
    def __init__(self,
                 result_file,
                 fault_file,
                 earth_file=None):
        super().__init__(result_file)

        self.fault_file = fault_file
        if fault_file is not None:
            reader = FaultFileReader(fault_file)
            self.num_subflt_along_strike = reader.num_subflt_along_strike
            self.num_subflt_along_dip = reader.num_subflt_along_dip
            self.num_subflts = self.num_subflt_along_strike * self.num_subflt_along_dip
            self.LLons_mid = reader.LLons_mid
            self.LLats_mid = reader.LLats_mid
            

        self.earth_file = earth_file

    def get_3d_incr_slip(self):
        nx = self.num_subflt_along_strike
        ny = self.num_subflt_along_dip
        slip = self.incr_slip
        slip = slip.reshape([self.num_epochs, ny, nx])

        return slip

    def get_3d_afterslip(self):
        incr_slip = self.get_3d_incr_slip()
        slip = [np.zeros_like(incr_slip[0,:,:])]
        for ii in incr_slip[1:,:,:]:
            slip.append(slip[-1]+ii)
        slip = np.asarray(slip)
        return slip

    def get_3d_cumu_slip(self):
        incr_slip = self.get_3d_incr_slip()
        slip = [incr_slip[0,:,:]]
        for ii in incr_slip[1:,:,:]:
            slip.append(slip[-1]+ii)
        slip = np.asarray(slip)
        return slip

    def get_cumu_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        return self.get_3d_cumu_slip()[nth,:,:] 
        
    def get_incr_slip_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_incr_slip_at_nth_epoch(idx)

    def get_incr_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < len(self.epochs)
        
        return self.get_3d_incr_slip()[nth,:,:]    

    def get_cumu_slip_Mos_Mws(self):
        assert self.earth_file is not None, 'Missing earth_file!'
        compute = MomentCalculator(self.fault_file, self.earth_file)
        epochs = self.epochs
        mos = []
        mws = []

        slip = self.get_3d_cumu_slip()
        
        for nth, epoch in enumerate(epochs):
            aslip = slip[nth,:,:]
            mo, mw = compute.compute_moment(aslip)
            mos.append(mo)
            mws.append(mw)
        return mos, mws, epochs

    def get_afterslip_Mos_Mws(self):
        assert self.earth_file is not None, 'Missing earth_file!'
        compute = MomentCalculator(self.fault_file, self.earth_file)
        epochs = self.epochs
        mos = []
        mws = []
        _epochs = []

        slip = self.get_3d_afterslip()
        
        for nth, epoch in enumerate(epochs):
            if epoch == 0:
                continue
            aslip = slip[nth,:,:]
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
