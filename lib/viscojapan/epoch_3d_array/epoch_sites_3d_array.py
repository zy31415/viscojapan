import h5py
import numpy as np
__author__ = 'zy'

from .epoch_3d_array import Epoch3DArray

class EpochSites3DArray(Epoch3DArray):
    def __init__(self,
                 array_3d,
                 epochs,
                 sites,
                 mask_sites = None):
        '''
        If you get data from this class, they are always filtered after the mask sites.
        :param array_3d: ndarray(dim=3)
        :param epochs: list
        :param sites: list
        :param mask_sites: list
        :return: object
        '''

        super().__init__(array_3d = array_3d,
                         epochs = epochs)

        self._sites = sites

        self.set_mask_sites(mask_sites)


    def assert_in_sites(self, sites):
        for s in sites:
            assert s in self._sites

    def get_sites(self):
        return self._sites

    def get_num_sites(self):
        return len(self._sites)

    def get_mask_sites(self):
        return self._mask_sites

    def get_num_mask_sites(self):
        return len(self._mask_sites)

    def set_mask_sites(self, mask_sites):
        if mask_sites is None:
            mask_sites = self.get_sites()
        self.assert_in_sites(mask_sites)
        self._mask_sites = mask_sites

    def get_mask(self):
        ch = []
        for site in self.mask_sites:
            ch.append(self.sites.index(site))
        ch = np.asarray(ch)
        return ch

    def get_array_3d(self):
        mask = self.get_mask()
        array_3d = super().get_array_3d()
        return array_3d[:,mask,:]

    def get_index_in_sites(self, site):
        return self._sites.index(site)

    def get_index_in_mask_sites(self, site):
        return self._mask_sites.index(site)

    @classmethod
    def load(cls,fn,
             mask_sites = None,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        with h5py.File(fn, 'w') as fid:
            if memory_mode:
                array_3d = fid['array3d'][...]
            else:
                array_3d = fid['array3d']

            epochs = fid['epochs'][...]

            sites = fid['sites'][...]

        return cls(array_3d = array_3d, epochs = epochs, sites = sites, mask_sites=mask_sites)

    def save(self, fn):
        super().save(fn)
        with h5py.File(fn) as fid:
            fid['sites'] = self._sites()





