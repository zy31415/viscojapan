__all__ = ['EpochFileReader']

class EpochFileReader(FileIOBase):
    ''' Use this class to CREATE and READ epochal data file.
'''
    def __init__(self,
                 file_name):
        super().__init__(file_name)

    def open(self):
        assert exists(self.file_name), "File must exists!"
        fid = h5py.File(self.file_name,'r')
        return fid

    def _assert_within_range(self,epoch):
        epochs = self.get_epochs()

        max_day = max(epochs)
        min_day = min(epochs)
        assert epoch <= max_day, 'Max day: %d'%max_day
        assert epoch >= min_day, 'Min day: %d'%min_day

    def get_epoch_value_no_interpolation(self, epoch):
        epochs = self.get_epochs()
        assert epoch in epochs, "Interpolation is not allowed in this method."
        out = self.fid['epochs/%04d'%epoch][...]
        return out

    def get_epoch_value(self, epoch):
        self._assert_within_range(epoch)
        epochs = self.get_epochs()
        if epoch in epochs:
            return self.get_epoch_value_no_interpolation(epoch)
        for nth, ti in enumerate(epochs[1:]):
            if epoch <= ti:
                break
        t1 = epochs[nth]
        t2 = epochs[nth+1]

        assert (t1<t2) and (t1<=epoch) and (epoch<=t2), \
               'Epoch %d should be in %d ~ %d'%(epoch, t1, t2)

        G1=self.get_epoch_value_no_interpolation(t1)
        G2=self.get_epoch_value_no_interpolation(t2)

        G=(epoch-t1)/(t2-t1)*(G2-G1)+G1

        return G

    def get_info(self, key, attr=None):
        if attr == None:
            assert self.has_info(key), "No key %s in file %s."\
                   %(key, self.file_name)
            out = self.fid['info/%s'%key][...]
        else:
            out = self.fid['info/%s'%key].attrs[attr][...]
        return out

    def get_epochs(self):
        out = sorted([int(ii) for ii in self.fid['epochs'].keys()])
        return out

    @property
    def epochs(self):
        return self.get_epochs()

    def has_info(self, key):
        return 'info/%s'%key in self.fid

    def iter_epoch_values(self):
        epochs = self.get_epochs()
        for epoch in epochs:
            yield epoch, self.get_epoch_value(epoch)

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.get_epoch_value(name)
        elif isinstance(name, str):
            return self.get_info(name)
        else:
            raise ValueError('Not recognized type.')



