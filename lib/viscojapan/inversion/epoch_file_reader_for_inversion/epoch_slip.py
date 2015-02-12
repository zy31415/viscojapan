import numpy as np

from .epoch_file_reader import EpochFileReader

__author__ = 'zy'
__al__ = ['EpochSlip']

def cumu3d_to_incr3d(cumu3d):
    res1 = cumu3d[:1,:,:]
    res2 = np.diff(cumu3d, axis=0)
    incr3d = np.concatenate([res1,res2], axis=0)
    return incr3d

class EpochSlip(EpochFileReader):
    def __init__(self, file_name):
        super().__init__(file_name)

        self.num_subflt_along_strike = self.data3d.shape[2]
        self.num_subflt_along_dip = self.data3d.shape[1]

    def get_cumu_slip_at_nth_epoch(self, nth):
        return self.data3d[nth,:,:][...]

    @property
    def incr_slip3d(self):
        return cumu3d_to_incr3d(self.data3d)

    def get_incr_slip_at_nth_epoch(self, nth):
        return self.incr_slip3d[nth]

    def stack(self, epochs):
        out1 = [self.get_data_at_epoch(epoch).reshape([-1,1]) for epoch in epochs]

        out2 = [out1[0]]
        for s1, s2 in zip(out1[0:], out1[1:]):
            out2.append(s2-s1)

        return np.vstack(out2)

