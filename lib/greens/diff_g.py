import h5py 

from .g_reader import GReader

class DiffG(object):
    ''' This class computes the diffrence of G with respcet to (wrt)
an indicated variable.
'''
    def __init__(self, obj1_epoch_file, obj2_epoch_file, wrt):
        ''' Arguments:
obj1_epoch_file : object of EpochFile
obj2_epoch_file : object of EpochFile
wrt - with respect to, variable that the change WRT.
'''
        self.obj1_epoch_file = obj1_epoch_file
        self.obj2_epoch_file = obj2_epoch_file
        self.wrt = wrt

    def _get_vars(self):
        self.var1 = float(self.obj1_epoch_file.get_info(wrt))
        setattr(self, self.wrt+'1', self.var1)

        self.var2 = float(self.obj2_epoch_file.get_info(wrt))
        setattr(self, self.wrt+'2', self.var2)

    def get_epoch_value(self, day):
        G1 = self.obj1_epoch_file.get_epoch_value(day)
        G2 = self.obj2_epoch_file.get_epoch_value(day)

        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG
        
