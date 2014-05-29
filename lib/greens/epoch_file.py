from os.path import exists

import h5py

class EpochFile(object):
    ''' This class defines an prototype of accessing a certain kind of
HDF5 files, which is used for storing large epochal data.

In this project, these information are stored and accessed
with this prototype:

(1) Green's function at different epochs.
(2) The difference of Green's function at different epochs with
    respect to certain variables (for example, viscosity or elastic
    depth)
'''
    def __init__(self,fG):
        self.fG = fG

    def set_epoch_value(self, time, value):
        assert isinstance(time,int)
        with h5py.File(self.fG,'a') as fid:
            fid['epochs/%04d'%time] = value

    def get_epoch_value(self, time):
        assert isinstance(time,int)
        with h5py.File(self.fG,'r') as fid:
            out = fid['epochs/%04d'%time][...]
        return out

    def set_info(self, key, value, **kwargs):
        ''' Set info. **args are attributs
'''
        with h5py.File(self.fG,'a') as fid:
            fid['info/%s'%key] = value        
            for key_attr, value_attr in kwargs.items():
                fid['info/%s'%key].attrs[key_attr] = value_attr

    def set_info_attr(self,key, key_attr, value_attr):
        with h5py.File(self.fG,'a') as fid:
            fid['info/%s'%key].attrs[key_attr] = value_attr

    def get_info(self, key, attr=None):
        if attr == None:
            with h5py.File(self.fG,'r') as fid:
                out = fid['info/%s'%key][...]
        else:
            with h5py.File(self.fG,'r') as fid:
                out = fid['info/%s'%key].attrs[attr][...]
        return out

    def get_epochs(self):
        with h5py.File(self.fG,'r') as fid:
            out = sorted([int(ii) for ii in fid['epochs'].keys()])
        return out
        
        
