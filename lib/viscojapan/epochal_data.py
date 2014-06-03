from os.path import exists

import h5py

class EpochalDataBase(object):
    ''' This class defines an prototype of accessing a certain kind of
HDF5 files, which is used for storing large epochal data.

In this project, these information are stored and accessed
with this prototype:

(1) Green's function at different epochs.
(2) The difference of Green's function at different epochs with
    respect to certain variables (for example, viscosity or elastic
    depth)
(3) observation : observed cumulative displacement.
(4) slip on the faults.
etc.
'''
    def __init__(self,epoch_file):
        self.epoch_file = epoch_file

    def set_epoch_value(self, time, value):
        assert isinstance(time,int)
        with h5py.File(self.epoch_file,'a') as fid:
            fid['epochs/%04d'%time] = value

    def get_epoch_value(self, epoch):
        assert isinstance(epoch,int), "Time should be int type."
        epochs = self.get_epochs()
        assert epoch in epochs, "Not in the database!"
        with h5py.File(self.epoch_file,'r') as fid:
            out = fid['epochs/%04d'%epoch][...]
        return out

    def set_info(self, key, value, **kwargs):
        ''' Set info. **args are attributs
'''
        with h5py.File(self.epoch_file,'a') as fid:
            fid['info/%s'%key] = value        
            for key_attr, value_attr in kwargs.items():
                fid['info/%s'%key].attrs[key_attr] = value_attr

    def set_info_dic(self, info_dic):
        for key, val in info_dic.items():
            self.set_info(key,val)

    def set_info_attr(self,key, key_attr, value_attr):
        with h5py.File(self.epoch_file,'a') as fid:
            fid['info/%s'%key].attrs[key_attr] = value_attr

    def get_info(self, key, attr=None):
        if attr == None:
            with h5py.File(self.epoch_file,'r') as fid:
                out = fid['info/%s'%key][...]
        else:
            with h5py.File(self.epoch_file,'r') as fid:
                out = fid['info/%s'%key].attrs[attr][...]
        return out

    def get_epochs(self):
        with h5py.File(self.epoch_file,'r') as fid:
            out = sorted([int(ii) for ii in fid['epochs'].keys()])
        return out

    def has_info(self, key):
        with h5py.File(self.epoch_file,'r') as fid:
            return 'info/%s'%key in fid
        
    def iter_epoch_values(self):
        epochs = self.get_epochs()
        for epoch in epochs:
            yield epoch, self.get_epoch_value(epoch)

    def copy_info_from_file(self, epoch_file):
        with h5py.File(epoch_file,'r') as from_file:
            with  h5py.File(self.epoch_file,'a') as to_file:
                from_file.copy('info/',to_file)


class EpochalData(EpochalDataBase):
    ''' This class can get value from a epoch file at any time.
'''
    def __init__(self, epoch_file):
        super().__init__(epoch_file)

    def _assert_within_range(self,day):
        days_of_epochs = self.get_epochs()
            
        max_day = max(days_of_epochs)
        min_day = min(days_of_epochs)
        assert day <= max_day, 'Max day: %d'%max_day
        assert day >= min_day, 'Min day: %d'%min_day
        
    def get_epoch_value(self, day):
        ''' Get G matrix at a certain day.
'''
        self._assert_within_range(day)

        days_of_epochs = self.get_epochs()
        
        if day in days_of_epochs:
            return super().get_epoch_value(day)
        
        for nth, ti in enumerate(days_of_epochs):
            if day <= ti:
                break

        t1 = days_of_epochs[nth-1]
        t2 = days_of_epochs[nth]
        
        G1=super().get_epoch_value(t1)
        G2=super().get_epoch_value(t2)

        G=(day-t1)/(t2-t1)*(G2-G1)+G1

        return G

