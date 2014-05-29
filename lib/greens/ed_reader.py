from os.path import exists

import h5py

from .epochal_data import EpochalData

class EDReader(EpochalData):
    ''' This class can get value from a epoch file at any time.
'''
    def __init__(self, epoch_file):
        super().__init__(epoch_file)
        assert exists(self.epoch_file), "File %s doesn't exist."%self.epoch_file
        
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
