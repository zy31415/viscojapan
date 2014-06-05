from os.path import exists

import h5py

class EpochalData(object):
    def __init__(self,epoch_file):
        self.epoch_file = epoch_file

    def set_epoch_value(self, time, value):
        assert isinstance(time,int)
        with h5py.File(self.epoch_file,'a') as fid:
            fid['epochs/%04d'%time] = value

    def _assert_within_range(self,epoch):
        epochs = self.get_epochs()
            
        max_day = max(epochs)
        min_day = min(epochs)
        assert epoch <= max_day, 'Max day: %d'%max_day
        assert epoch >= min_day, 'Min day: %d'%min_day

    def get_epoch_value(self, epoch):
        self._assert_within_range(epoch)
        
        epochs = self.get_epochs()

        if epoch in epochs:
            with h5py.File(self.epoch_file,'r') as fid:
                out = fid['epochs/%04d'%epoch][...]
            return out
        else:                                 
            for nth, ti in enumerate(epochs):
                if epoch <= ti:
                    break
            t1 = epochs[nth-1]
            t2 = epochs[nth]
            
            G1=self.get_epoch_value(t1)
            G2=self.get_epoch_value(t2)

            G=(epoch-t1)/(t2-t1)*(G2-G1)+G1

            return G

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

    def copy_info_from(self, epoch_file):
        with h5py.File(epoch_file,'r') as from_file:
            with  h5py.File(self.epoch_file,'a') as to_file:
                from_file.copy('info/',to_file)

    def copy_info_to(self, epoch_file):
        with h5py.File(self.epoch_file,'r') as from_file:
            with  h5py.File(epoch_file,'a') as to_file:
                from_file.copy('info/',to_file)


