import numpy as np
import h5py

__author__ = 'zy'
__all__ = ['Epoch3DArray']

def _assert_within_range(epochs,epoch):
    max_day = max(epochs)
    min_day = min(epochs)
    assert epoch <= max_day, 'Max day: %d'%max_day
    assert epoch >= min_day, 'Min day: %d'%min_day

def _assert_ascending(arr):
    assert all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

class _Epoch3DArray(object):
    HDF5_DATASET_NAME_FOR_3D_ARRAY = 'data3d'
    def __init__(self,
                 array_3d,
                 epochs):
        assert len(array_3d.shape) == 3
        self._array_3d = array_3d

        self._epochs = list(epochs)
        assert array_3d.shape[0] == len(self._epochs)
        _assert_ascending(epochs)

        self.num_epochs = len(self._epochs)

    def get_array_3d(self):
        '''
        Note - This is the only data fetch function that directly accesses the private variable member _array_3d.
        All other data fetch functions access the core 3d data through this method.
        Therefore, if you change the behavior of this function through overriding in the subclasses, then all the
         behaviour of other data fetch functions will be affected.

         This is how I implement the mask sites functionality - overriding function get_array_3d and applying a mask
         onto its outputs.
         .
        :return: ndarray(dim=3)
        '''
        return self._array_3d

    def get_epochs(self):
        return self._epochs

    # Serialization
    def save(self, fn):
        with h5py.File(fn, 'w') as fid:
            fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY] = self._array_3d[...]
            fid['epochs'] = self._epochs

    @classmethod
    def load(cls,fid,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        if memory_mode:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        else:
            array_3d = fid[cls.HDF5_DATASET_NAME_FOR_3D_ARRAY]

        epochs = fid['epochs'][...]

        return cls(array_3d=array_3d, epochs=epochs)



# functions in this class are not allowed to access the private variables:
#  _array_3d and _epochs
# This is why I design a new class based on _Epoch3DArray.
#
class Epoch3DArray(_Epoch3DArray):
    def __init__(self,
                 array_3d,
                 epochs):

        super().__init__(array_3d=array_3d,
                         epochs=epochs)

    def get_velocity_3d(self):
        dt = np.diff(self.get_epochs()).reshape([-1,1,1])
        vel = np.diff(self.get_array_3d(), axis=0)/dt
        return vel

    # Get data at an epoch
    def get_data_at_nth_epoch(self, nth):
        '''
        :param nth: int
        :return: np.ndarray
        '''
        return self.get_array_3d()[nth,:,:]

    def get_data_at_epoch_no_interpolation(self, epoch):
        '''
        :param epoch: int
        :return: np.ndarray
        '''
        epochs = self.get_epochs()
        nth = epochs.index(epoch)
        return self.get_data_at_nth_epoch(nth)

    def get_data_at_epoch(self, epoch):
        epochs = self.get_epochs()
        self._assert_epoch_within_range(epoch)
        if epoch in epochs:
            return self.get_data_at_epoch_no_interpolation(epoch)

        for nth, ti in enumerate(epochs[1:]):
            if epoch <= ti:
                break

        t1 = epochs[nth]
        t2 = epochs[nth+1]

        val1 = self.get_array_3d()[nth, :, :]
        val2 = self.get_array_3d()[nth, :, :]

        val = (epoch-t1) / (t2-t1) * (val2-val1) + val1

        return val

    def __getitem__(self, name):
        return self.get_data_at_epoch(name)

    def _assert_epoch_within_range(self, epoch):
        epochs = self.get_epochs()
        max_day = max(epochs)
        min_day = min(epochs)
        assert epoch <= max_day, 'Max day: %d'%max_day
        assert epoch >= min_day, 'Min day: %d'%min_day









