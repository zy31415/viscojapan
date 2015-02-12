import numpy as np

from .epoch_file_reader import EpochFileReader

__author__ = 'zy'
__al__ = ['EpochalSlip']

class EpochalSlip(EpochFileReader):
    def __init__(self, file_name):
        super().__init__(file_name)

    def stack(self, epochs):
        out1 = [self.get_data_at_epoch(epoch).reshape([-1.1]) for epoch in epochs]
        out2 = [out1[0]]
        for s1, s2 in zip(out1[0:], out2[1:]):
            out2.append(s2-s1)

        return np.vstack(out2)

