from os.path import exists

import h5py

__author__ = 'zy'

class EpochFileReader(object):
    ''' Use this class to CREATE and READ epochal data file.
'''
    def __init__(self,
                 file_name):
        self.file_name = file_name
        self.fid = self.open()

        self.data3d = self.fid['data3d']
        self._epochs = self.fid['epochs'][...]

        assert self.data3d.shape[0] == self.num_epochs

    def open(self):
        assert exists(self.file_name), "File %s not exists!"%self.file_name
        fid = h5py.File(self.file_name,'r')
        return fid

    def close(self):
        if self.fid is not None:
            self.fid.close()
        self.fid = None

    @property
    def epochs(self):
        return self._epochs

    @property
    def num_epochs(self):
        return len(self.epochs)

    def _assert_within_range(self,epoch):
        epochs = self.epochs

        max_day = max(epochs)
        min_day = min(epochs)
        assert epoch <= max_day, 'Max day: %d'%max_day
        assert epoch >= min_day, 'Min day: %d'%min_day

    def get_data_at_epoch_no_interpolation(self, epoch):
        epochs = self.epochs
        assert epoch in epochs, "Interpolation is not allowed in this method."
        out = self.data3d[self.epochs == epoch,:,:]
        assert out.shape[0] == 1
        return out[0,:,:]

    def get_data_at_epoch(self, epoch):
        self._assert_within_range(epoch)
        epochs = self.epochs
        if epoch in epochs:
            return self.get_data_at_epoch_no_interpolation(epoch)

        for nth, ti in enumerate(epochs[1:]):
            if epoch <= ti:
                break

        t1 = epochs[nth]
        t2 = epochs[nth+1]

        assert (t1<t2) and (t1<=epoch) and (epoch<=t2), 'Epoch %d should be in %d ~ %d'%(epoch, t1, t2)

        G1=self.get_data_at_epoch_no_interpolation(t1)
        G2=self.get_data_at_epoch_no_interpolation(t2)

        G=(epoch-t1)/(t2-t1)*(G2-G1)+G1

        return G

    def get_info(self, key, attr=None):
        if attr == None:
            assert self.has_info(key), "No key %s in file %s."\
                   %(key, self.file_name)
            out = self.fid[key][...]
        else:
            out = self.fid[key].attrs[attr][...]
        return out

    def has_info(self, key):
        return key in self.fid

    def __getitem__(self, name):
        if isinstance(name, int):
            return self.get_data_at_epoch(name)
        elif isinstance(name, str):
            return self.get_info(name)
        else:
            raise ValueError('Not recognized type.')

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()



