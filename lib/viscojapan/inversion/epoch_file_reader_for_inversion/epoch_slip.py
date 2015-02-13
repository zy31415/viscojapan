import h5py

import numpy as np

from ...epoch_3d_array import Slip

__author__ = 'zy'
__al__ = ['EpochSlip']


class EpochSlip(Slip):

    def __init__(self, file_name):

        fid = h5py.File(file_name, 'r')
        cumu_slip_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        epochs = list(fid['epochs'][...])

        super().__init__(cumu_slip_3d = cumu_slip_3d,
                         epochs = epochs)

    def stack(self, epochs):
        out1 = [self.get_cumu_slip_at_epoch(epoch).reshape([-1,1]) for epoch in epochs]
        out2 = [out1[0]]
        for s1, s2 in zip(out1[0:], out1[1:]):
            out2.append(s2-s1)
        return np.vstack(out2)

