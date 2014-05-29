'''
'''
from os.path import exists

import h5py

from .epoch_file import EpochFile

def _assert_ascending_order(alist):
    leng = len(alist)
    assert all(alist[ii] <= alist[ii+1] for ii in range(leng - 1)), \
           "The list is not in ascending order!"
    

class GReader(EpochFile):
    ''' This class read and a G file and do temporal interpolation.
Use sites_file to indicate which stations you want to use.
'''
    def __init__(self, fG):
        super().__init__(fG)
        assert exists(self.fG), "File %s doesn't exist."%self.fG
        
        self.sites_file = ''
        self._init()
        
    def _init(self):
        ''' Initialization of the class.
'''
        self._init_site_file()    
        
    def _init_site_file(self):
        sites_original = self.get_info('sites')
        if self.sites_file != '':
            assert exists(self.sites_file), "sites file doesn't exist."
            sites = loadtxt(self.sites_file,'4a')
            for site in sites:
                assert site in sites_original, 'No data about %s.'%site
            self.sites = sites
        else:
            self.sites = sites_original
            
    def get(self, day):
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
        
        G1=self.get_epoch_value(t1)
        G2=self.get_epoch_value(t2)

        G=(day-t1)/(t2-t1)*(G2-G1)+G1
        return G

if __name__ == '__main__':
    a=[1,2,3,4,1]
    _assert_ascending_order(a)
