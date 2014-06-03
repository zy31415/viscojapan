from os.path import join, exists
import sys

from numpy import loadtxt, nan_to_num

sys.path.append('/home/zy/workspace/greens/lib/')
from greens.epochal_data import EpochalData

class ObsToEpochalData(EpochalData):
    def __init__(self, epoch_file):
        super().__init__(epoch_file)
        self.dir_obs_txt = ''
        self.epochs = []

        self.file_sites = ''

    def _init(self):
        assert not exists(self.epoch_file), \
               "Output file %s exists already!"%self.epoch_file
        for day in self.epochs:
            assert exists(self._form_filename(day)),\
                   "Inputs file %s does not exist!"%day

    def _form_filename(self,epoch):
        return join(self.dir_obs_txt,'%04d'%epoch)

    def _read_a_txt(self,epoch):
        data = loadtxt(self._form_filename(epoch))
        data = nan_to_num(data)
        return data.reshape([-1,1])

    def _set_info(self):
        self.set_info('sites',loadtxt(self.file_sites,'4a'))
        
    def __call__(self):
        self._init()
        for epoch in self.epochs:
            print(epoch)
            self.set_epoch_value(epoch, self._read_a_txt(epoch))

        self._set_info()
