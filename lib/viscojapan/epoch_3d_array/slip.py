__author__ = 'zy'

import numpy as np

from .epoch_3d_array import Epoch3DArray

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


class Slip(Epoch3DArray):
    def __init__(self,
                 cumu_slip_3d,
                 epochs
                 ):

        assert epochs[0] == 0, 'The class is designed to represent slip that starts at t=0.'

        super().__init__(array3d = cumu_slip_3d,
                         epochs = epochs
        )

        slip_shape = self.get_array_3d.shape
        self.num_subflt_along_strike = slip_shape[2]
        self.num_subflt_along_dip = slip_shape[1]

    # constructors
    @classmethod
    def init_with_incr_slip_3d(cls, incr3d, epochs):
        cumu3d = incr3d_to_cumu3d(incr3d)
        return cls(cumu3d=cumu3d, epochs=epochs)

    @classmethod
    def init_with_cumu_slip_3d(cls, cumu3d, epochs):
        return cls(cumu3d=cumu3d, epochs=epochs)

    # return slip as 3d array
    @property
    def incr_slip_3d(self):
        return cumu3d_to_incr3d(self.cumu_slip_3d)

    @property
    def afterslip_3d(self):
        # note that for a dataset object of hdf5 file,
        # this operation is between the dataset object and a ndarray object.
        return self.cumu_slip_3d - self.cumu_slip_3d[0,:,:]

    @property
    def cumu_slip_3d(self):
        return self.get_array_3d

    # return slip at a time slice:
    def get_coseismic_slip(self):
        return self.cumu_slip_3d[0,:,:]

    def get_cumu_slip_at_nth_epoch(self, nth):
        self.get_data_at_nth_epoch(nth)

    def get_cumu_slip_at_epoch(self, epoch):
        return self.get_data_at_epoch(epoch)

    def get_incr_slip_at_nth_epoch(self, nth):
        return self.incr_slip_3d[nth,:,:]

    def get_incr_slip_at_epoch(self, epoch):
        assert epoch in self.get_epochs, 'Epoch %d is not in the epochs.'%epoch
        idx = self.get_epochs.index(epoch)
        return self.get_incr_slip_at_nth_epoch(idx)

    def get_afterslip_at_nth_epoch(self, nth):
        nth = int(nth)
        assert nth>=0
        assert nth < self.num_epochs

        return self.afterslip_3d[nth,:,:]

    def get_slip_rate_at_nth_epoch(self, nth):
        if nth == 0:
            # rate of coseismic slip is infinite
            slip_rate = self.incr_slip_3d[0,:,:] + np.inf
        else:
            slip_rate = self.get_velocity_3d[nth-1,:,:]
        return slip_rate

    # get sip history at a subfault
    def get_incr_slip_at_subfault(self, nth_dip, nth_stk):
        return self.incr_slip_3d[:, nth_dip, nth_stk]

    def get_cumu_slip_at_subfault(self, nth_dip, nth_stk):
        return self.cumu_slip_3d[:, nth_dip, nth_stk]

    def get_afterslip_at_subfault(self, nth_dip, nth_stk):
        return self.afterslip_3d[:, nth_dip, nth_stk]

    def get_slip_rate_at_subfault(self, nth_dip, nth_stk):
        return self.get_velocity_3d[:,nth_dip, nth_stk]

    def respace(self, epochs):
        '''
        Respace current object and return a new one.
        :param epochs: list
        :return: Epoch3DArray
        '''
        if list(epochs) == self.get_epochs:
            return self

        return self.__init__(
            array3d = np.dstack([self.get_data_at_epoch(t) for t in epochs]),
            epochs = epochs
            )








