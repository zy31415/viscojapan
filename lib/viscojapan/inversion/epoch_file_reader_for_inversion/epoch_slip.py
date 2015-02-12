import h5py

import numpy as np

from ...slip import Slip

__author__ = 'zy'
__al__ = ['EpochSlip']


class EpochSlip(Slip):
    @classmethod
    def init_from_file(cls, file_name):
        fid = h5py.File(file_name, 'r')
        return cls.init_from_cumu3d(fid['data3d'], list(fid['epochs'][...]))

    def stack(self, epochs):
        out1 = [self.get_cumu_slip_at_epoch(epoch).reshape([-1,1]) for epoch in epochs]
        out2 = [out1[0]]
        for s1, s2 in zip(out1[0:], out1[1:]):
            out2.append(s2-s1)
        return np.vstack(out2)

