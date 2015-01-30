__author__ = 'zy'

import numpy as np

__all__ = ['Slip']

def incr3d_to_cumu3d(incr3d):
    cumu3d = [incr3d[0,:,:]]
    for ii in incr3d[1:,:,:]:
        cumu3d.append(cumu3d[-1]+ii)
    cumu3d = np.asarray(cumu3d)
    return cumu3d

def cumu3d_to_incr3d(cumu3d):
    res1 = cumu3d[:1,:,:]
    res2 = np.diff(cumu3d, axis=0)
    incr3d = np.concatenate([res1,res2], axis=0)
    return incr3d

class Slip(object):
    def __init__(self,
                 incr3d,
                 epochs
                 ):
        # store cumulative slip instead of incremental slip, because it's easies to interpolate cumulative slip
        self.init_from_incr3d(incr3d, epochs)

    def init_from_incr3d(self, incr3d, epochs):
        self._cumu3d = incr3d_to_cumu3d(incr3d)
        self._epochs = epochs
        self._init()

    def init_from_cumu3d(self, cumu3d, epochs):
        self._cumu3d = cumu3d
        self.epochs = epochs
        self._init()

    def _init(self):
        slip_shape = self._cumu3d.shape
        # assert that self._incr_slip is a 3D array
        assert len(slip_shape) == 3

        self.num_subflt_along_strike = slip_shape[2]
        self.num_subflt_along_dip = slip_shape[1]
        self.num_epochs = len(self.epochs)
        assert slip_shape[0] == self.num_epochs


    def get_coseismic_slip(self):
        # assert the first element in self.epochs is 0.
        assert self.epochs[0] == 0
        return self._cumu3d[0]

    @property
    def incr_slip3d(self):
        return cumu3d_to_incr3d(self._cumu3d)

    @property
    def afterslip3d(self):
        return self.cumu_slip3d - self.cumu_slip3d[0,:,:]

    @property
    def cumu_slip3d(self):
        return self._cumu3d

    @property
    def epochs(self):
        return self._epochs

    def get_incr_slip_at_nth_epoch(self, nth):
        return self.incr_slip3d[nth]

    def get_incr_slip_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_incr_slip_at_nth_epoch(idx)

    def get_cumu_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < self.num_epochs

        return self.cumu_slip3d[nth,:,:]

    def get_cumu_slip_at_subfault(self, nth_dip, nth_stk):
        return self.cumu_slip3d[:, nth_dip, nth_stk]        

    def get_afterslip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < self.num_epochs

        return self.afterslip3d[nth,:,:]

    def get_slip_rate_at_nth_epoch(self, nth):
        if nth == 0:
            # rate of coseismic slip is infinite
            slip_rate = self.incr_slip3d[0,:,:] + np.inf
        else:
            assert nth>0
            assert nth < self.num_epochs
            delta_t = self.epochs[nth] - self.epochs[nth-1]
            slip_rate = self.incr_slip3d[nth]/delta_t
        return slip_rate


