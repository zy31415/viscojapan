'''
'''
from os.path import exists

import h5py


def _assert_ascending_order(alist):
    leng = len(alist)
    assert all(alist[ii] <= alist[ii+1] for ii in range(leng - 1)), \
           "The list is not in ascending order!"
    

class GReader(object):
    ''' This class read and a G file and do temporal interpolation.
'''
    def __init__(self, fG):
        assert exists(fG), "File %s doesn't exist."%fG
        self.fG = fG

        self._init()
        
    def _init(self):
        with h5py.File(self.fG,'r') as fid:
            days_of_epochs = fid['/info/days_of_epochs'][...]

            _assert_ascending_order(days_of_epochs)
            assert days_of_epochs[0]==0, 'The first day is not zero.'

            self.days_of_epochs = days_of_epochs
            self.max_day = max(self.days_of_epochs)

    def get(self, day):
        ''' Get G matrix at a certain day.
'''
        assert day >= 0
        assert day <= self.max_day

        days_of_epochs = self.days_of_epochs
        for nth, ti in enumerate(days_of_epochs):
            if day <= ti:
                break

        t1 = days_of_epochs[nth-1]
        t2 = days_of_epochs[nth]
        
        with h5py.File(self.fG,'r') as fid:
            G1=fid['%04d'%t1][...]
            G2=fid['%04d'%t2][...]

        G=(day-t1)/(t2-t1)*(G2-G1)+G1
        return G

if __name__ == '__main__':
    a=[1,2,3,4,1]
    _assert_ascending_order(a)
