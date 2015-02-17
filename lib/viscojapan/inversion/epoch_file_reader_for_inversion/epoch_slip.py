import h5py

import numpy as np

from ...epoch_3d_array import Slip

__author__ = 'zy'
__al__ = ['EpochSlip']


class EpochSlip(Slip):

    def __init__(self,
                 file_name = None,
                 cumu_slip_3d = None,
                 epochs = None,
                 memory_mode = False):

        if cumu_slip_3d is None:
            fid = h5py.File(file_name, 'r')

            if memory_mode:
                cumu_slip_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
            else:
                cumu_slip_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY]

            epochs = list(fid['epochs'][...])

        super().__init__(cumu_slip_3d = cumu_slip_3d,
                         epochs = epochs)

    def stack(self):
        epochs = self.get_epochs()
        return np.vstack([self.get_incr_slip_at_epoch(epoch).reshape([-1,1]) for epoch in epochs])

