__author__ = 'zy'

import numpy as np

__all__ = ['Slip']

class Slip(object):
    def __init__(self,
                 incr_slip,
                 epochs
                 ):
        self._incr_slip = incr_slip
        slip_shape = self._incr_slip.shape
        # assert that self._incr_slip is a 3D array
        assert len(slip_shape) == 3

        self.epochs = epochs

        self.num_subflt_along_strike = slip_shape[2]
        self.num_subflt_along_dip = slip_shape[1]
        self.num_epochs = len(self.epochs)
        assert slip_shape[0] == self.num_epochs


    def get_coseismic_slip(self):
        # assert the first element in self.epochs is 0.
        assert self.epochs[0] == 0
        return self._incr_slip[0]

    def get_3d_incr_slip(self):
        return self._incr_slip

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

    def get_incr_slip_at_nth_epoch(self, nth):
        return self._incr_slip[nth]

    def get_incr_slip_at_epoch(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = epochs.index(epoch)
        return self.get_incr_slip_at_nth_epoch(idx)

    def get_cumu_slip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < self.num_epochs

        return self.get_3d_cumu_slip()[nth,:,:]

    def get_afterslip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < self.num_epochs

        return self.get_3d_afterslip()[nth,:,:]

    def get_slip_rate_at_nth_epoch(self, nth):
        if nth == 0:
            # rate of coseismic slip is infinite
            slip_rate = self._incr_slip[0,:,:] + np.inf
        else:
            assert nth>0
            assert nth < self.num_epochs
            delta_t = self.epochs[nth] - self.epochs[nth-1]
            slip_rate = self._incr_slip[nth]/delta_t
        return slip_rate






