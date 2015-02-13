import numpy as np
import h5py

from ...utils import as_string

from ...epoch_3d_array import G as GClass

__author__ = 'zy'
__all__ = ['EpochG','DifferentialG']

def stack_G_for_convolution(self, epochs):
    N = len(epochs)
    x = self.get_data_at_epoch(0)
    sh1, sh2 = self.get_data_at_epoch(0).shape
    G = np.zeros((sh1*N, sh2*N), dtype='float')
    for nth in range(0, N):
        t1 = epochs[nth]
        for mth in range(nth, N):
            t2 = epochs[mth]
            #print(t2,t1,t2-t1)
            G_ = self.get_data_at_epoch(t2-t1)
            #print(mth*sh1,(mth+1)*sh1,nth*sh2,(nth+1)*sh2)
            G[mth*sh1:(mth+1)*sh1,
              nth*sh2:(nth+1)*sh2] = G_
    return G


class EpochG(GClass):
    def __init__(self,file_name,
                 mask_sites=None,
                 memory_mode = False):

        fid = h5py.File(file_name,'r')

        if memory_mode:
            array_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY][...]
        else:
            array_3d = fid[self.HDF5_DATASET_NAME_FOR_3D_ARRAY]

        epochs = fid['epochs'][...]
        sites = as_string(fid['sites'][...])

        super().__init__(g_3d = array_3d,
                        epochs = epochs,
                        sites = sites,
                        mask_sites = mask_sites)

        self.fid = fid

    def has_info(self, key):
        return key in self.fid

    def get_info(self, key):
        return self.fid[key][...]

    def __getitem__(self, name):
        if isinstance(name, int):
            return self[name]
        elif isinstance(name, str):
            return self.get_info(name)
        else:
            raise ValueError('Not recognized type.')

    stack = stack_G_for_convolution



class DifferentialG(object):
    ''' This class computes the diffretial of two EpochData objects
with respcet to (wrt) the change of an indicated variable.
'''
    def __init__(self, ed1, ed2, wrt):
        ''' Arguments:
ed1 : object of EpochalData
ed2 : object of EpochalData
wrt - with respect to, variable that the change WRT.
'''
        self.ed1 = ed1
        self.ed2 = ed2
        self.wrt = wrt

        self._init()

    def _init(self):
        assert self.ed1.has_info(self.wrt)
        assert self.ed2.has_info(self.wrt)

        self._get_vars()

    def _get_vars(self):
        self.var1 = float(self.ed1.get_info(self.wrt))
        setattr(self, self.wrt+'1', self.var1)

        self.var2 = float(self.ed2.get_info(self.wrt))
        setattr(self, self.wrt+'2', self.var2)

    def get_data_at_epoch(self, day):
        G1 = self.ed1.get_data_at_epoch(day)
        G2 = self.ed2.get_data_at_epoch(day)
        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.get_data_at_epoch(name)
        else:
            raise ValueError('Not recognized type.')

    # Monkey Patch :-)
    stack = stack_G_for_convolution