import numpy as np
import h5py

__author__ = 'zy'

def _assert_within_range(epochs,epoch):
    max_day = max(epochs)
    min_day = min(epochs)
    assert epoch <= max_day, 'Max day: %d'%max_day
    assert epoch >= min_day, 'Min day: %d'%min_day

def _assert_ascending(arr):
    assert all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

class Epoch3DArray(object):
    def __init__(self,
                 array_3d,
                 epochs):

        assert len(array_3d.shape) == 3
        self._array_3d = array_3d

        self._epochs = list(epochs)
        assert array_3d.shape[0] == len(self._epochs)
        _assert_ascending(epochs)

        self.num_epochs = len(self._epochs)

    @property
    def array_3d(self):
        return self._array_3d

    @property
    def velocity_3d(self):
        dt = np.diff(self.epochs).reshape([-1,1,1])
        vel = np.diff(self.array_3d, axis=0)/dt
        return vel

    @property
    def epochs(self):
        return self._epochs


    # Serialization
    def save(self, fn):
        with h5py.File(fn, 'w') as fid:
            fid['array3d'] = self.array_3d
            fid['epochs'] = self.epochs

    @classmethod
    def load(cls,fn,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        with h5py.File(fn, 'w') as fid:
            if memory_mode:
                array3d = fid['array3d'][...]
            else:
                array3d = fid['array3d']

            epochs = fid['epochs'][...]

        return cls(array3d, epochs)

    # Get data at an epoch
    def get_data_at_nth_epoch(self, nth):
        '''
        :param nth: int
        :return: np.ndarray
        '''
        return self._array_3d[nth,:,:]

    def get_data_at_epoch_no_interpolation(self, epoch):
        '''
        :param epoch: int
        :return: np.ndarray
        '''
        assert epoch in self.epochs
        idx = self.epochs.index(epoch)
        return self.array_3d[idx,:,:]

    def get_data_at_epoch(self, epoch):
        if epoch in self.epochs:
            return self.get_data_at_epoch_no_interpolation(epoch)

        for nth, ti in enumerate(self.epochs[1:]):
            if epoch <= ti:
                break

        t1 = self.epochs[nth]
        t2 = self.epochs[nth+1]

        val1 = self.array_3d[nth, :, :]
        val2 = self.array_3d[nth, :, :]

        val = (epoch-t1) / (t2-t1) * (val2-val1) + val1

        return val

    def respace(self, epochs):
        '''
        Respace current object and return a new one.
        :param epochs: list
        :return: Epoch3DArray
        '''
        if list(epochs) == self.epochs:
            return self

        return self.__init__(
            array3d = np.dstack([self.get_data_at_epoch(t) for t in epochs]),
            epochs = epochs
            )









