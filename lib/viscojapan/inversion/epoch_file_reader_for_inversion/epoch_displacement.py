import numpy as np
import h5py

from ...epoch_3d_array import Displacement
from ...utils import as_string

__author__ = 'zy'
__all__ = ['EpochDisplacement', 'EpochDisplacementSD']

class EpochDisplacement(Displacement):
    def __init__(self,
                 file_name,
                 mask_sites=None,
                 memory_mode = False):

        fid = h5py.File(file_name,'r')

        if memory_mode:
            array_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        else:
            array_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY]

        epochs = fid['epochs'][...]
        sites = as_string(fid['sites'][...])

        super().__init__(cumu_disp_3d = array_3d,
                        epochs = epochs,
                        sites = sites,
                        mask_sites = mask_sites)

    def stack(self, epochs):
        return np.vstack([self.get_data_at_epoch(epoch).reshape([-1,1]) for epoch in epochs])


class EpochDisplacementSD(EpochDisplacement):
    def __init__(self,file_name,
                 mask_sites=None,
                 memory_mode = False):
        super().__init__(file_name, mask_sites, memory_mode)

    def get_data_at_epoch(self, epoch):
        assert epoch in self.get_epochs(), "EpochalDisplacementSD doesn't allow interpolation."
        return super().get_data_at_epoch(epoch)