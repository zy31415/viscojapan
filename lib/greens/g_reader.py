'''
'''
from os.path import exists

import h5py
from numpy import asarray, loadtxt

from .epoch_file import EpochFile

class GReader(EpochFile):
    ''' This class extends EpochFile class to get G matrix value at any time.
'''
    def __init__(self, fG):
        super().__init__(fG)
        assert exists(self.fG), "File %s doesn't exist."%self.fG
        
    def get_epoch_value(self, day):
        ''' Get G matrix at a certain day.
'''
        assert day >= 0
        days_of_epochs = self.get_epochs()
        max_day = max(days_of_epochs)
        assert day <= max_day, 'Max day: %d'%max_day

        
        for nth, ti in enumerate(days_of_epochs):
            if day <= ti:
                break

        t1 = days_of_epochs[nth-1]
        t2 = days_of_epochs[nth]
        
        G1=super().get_epoch_value(t1)
        G2=super().get_epoch_value(t2)

        G=(day-t1)/(t2-t1)*(G2-G1)+G1

        return G

    def set_epoch_value(self,day,value):
        raise ValueError('This is a reader only!')
