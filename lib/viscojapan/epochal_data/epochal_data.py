from os.path import exists

import h5py

class EpochalData(object):
    ''' Use this class to CREATE and READ epochal data file.
'''
    def __init__(self,
                 epoch_file):
        self.epoch_file = epoch_file

    def set_epoch_value(self, time, value):
        assert isinstance(time,int), 'Time %s is not integer.'%(str(time))
        with h5py.File(self.epoch_file,'a') as fid:
            fid['epochs/%04d'%time] = value

    def set_value(self, epoch, index, value):
        with h5py.File(self.epoch_file, 'a') as fid:
            fid['epochs/%04d'%epoch][index] = value

    def _assert_within_range(self,epoch):
        epochs = self.get_epochs()
            
        max_day = max(epochs)
        min_day = min(epochs)
        assert epoch <= max_day, 'Max day: %d'%max_day
        assert epoch >= min_day, 'Min day: %d'%min_day

    def _get_epoch_value(self, epoch):
        epochs = self.get_epochs()
        assert epoch in epochs, "Interpolation is not allowed in this method."
        with h5py.File(self.epoch_file,'r') as fid:
            out = fid['epochs/%04d'%epoch][...]
        return out
    
    def get_epoch_value(self, epoch):
        self._assert_within_range(epoch)
        epochs = self.get_epochs()
        if epoch in epochs:
            return self._get_epoch_value(epoch)
        for nth, ti in enumerate(epochs[1:]):
            if epoch <= ti:
                break
        t1 = epochs[nth]
        t2 = epochs[nth+1]

        assert (t1<t2) and (t1<=epoch) and (epoch<=t2), \
               'Epoch %d should be in %d ~ %d'%(epoch, t1, t2)
        
        G1=self._get_epoch_value(t1)
        G2=self._get_epoch_value(t2)

        G=(epoch-t1)/(t2-t1)*(G2-G1)+G1

        return G

    def __call__(self,epoch):
        return self.get_epoch_value(epoch)

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
            if 'info' in from_file:
                with  h5py.File(self.epoch_file,'a') as to_file:
                    from_file.copy('info/',to_file)

    def copy_info_to(self, epoch_file):
        with h5py.File(self.epoch_file,'r') as from_file:
            if 'info' in from_file:
                with  h5py.File(epoch_file,'a') as to_file:
                    from_file.copy('info/',to_file)

    def respacing(self, epochs, out_file):
        ep = EpochalData(out_file)
        for epoch in epochs:
            ep[epoch] = self[epoch]
        self.copy_info_to(out_file)

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.get_epoch_value(name)
        elif isinstance(name, str):
            return self.get_info(name)
        else:
            raise ValueError('Not recognized type.')

    def __setitem__(self, name, val):
        if isinstance(name, int):
            return self.set_epoch_value(name, val)
        elif isinstance(name, str):
            return self.set_info(name, val)
        else:
            raise ValueError('Not recognized type.')
    


