import h5py
import numpy as np

__author__ = 'zy'
__all__ = ['EpochSites3DArray']

from .epoch_3d_array import Epoch3DArray

def if_ascending(ll):
    if len(ll) == 1:
        return True
    return all(ll[i] <= ll[i+1] for i in range(len(ll)-1))

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
        for site in self._mask_sites:
            ch.append(self._sites.index(site))
        ch = np.asarray(ch)
        return list(ch)

    def get_index_in_sites(self, site):
        return self._sites.index(site)

    def get_index_in_mask_sites(self, site):
        return self._mask_sites.index(site)

    def get_array_3d(self):
        ''' This function overrides get_array_3d, which will mask outputs according to the mask array.
        :return: ndarray(dim=3)
        '''
        '''
        :return:
        '''
        mask = self.get_mask()
        array_3d = super().get_array_3d()

        # return array_3d[:,mask,:]

        # faster if mask is ascending
        if if_ascending(mask):
            return array_3d[:,mask,:]

        # slower if mask is not ordered.
        return np.hstack([array_3d[:,(mi,),:] for mi in mask])

    @classmethod
    def load(cls,fid,
             mask_sites = None,
             memory_mode = False # if memory_mode is True, all the data will be loaded into memory.
    ):
        epoch_array = Epoch3DArray.load(fid=fid, memory_mode=memory_mode)

        sites = fid['sites'][...]
        sites = [site.decode() for site in sites]

        return cls(array_3d = epoch_array.get_array_3d(),
                   epochs = epoch_array.get_epochs(),
                   sites = sites,
                   mask_sites=mask_sites)

    def save(self, fn):
        super().save(fn)
        with h5py.File(fn) as fid:
            sites = self.get_sites()
            sites = [site.encode() for site in sites]
            fid['sites'] = sites





