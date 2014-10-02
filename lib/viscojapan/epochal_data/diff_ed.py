import h5py 
from .stacking import conv_stack

class DiffED(object):
    ''' This class computes the diffretial of two EpochData objects
with respcet to (wrt) the change of an indicated variable.
'''
    def __init__(self, ed1, ed2, wrt):
        ''' Arguments:
ed1 : object of EpochalData
ed2 : object of EpochalData
wrt - with respect to, variable that the change WRT.
'''
        self.ed1 = ed1
        self.ed2 = ed2
        self.wrt = wrt

        self._init()
        
    def _init(self):
        assert self.ed1.has_info(self.wrt)
        assert self.ed2.has_info(self.wrt)
        
        self._get_vars()

    def _get_vars(self):
        self.var1 = float(self.ed1.get_info(self.wrt))
        setattr(self, self.wrt+'1', self.var1)

        self.var2 = float(self.ed2.get_info(self.wrt))
        setattr(self, self.wrt+'2', self.var2)

    def get_epoch_value(self, day):
        G1 = self.ed1.get_epoch_value(day)
        G2 = self.ed2.get_epoch_value(day)
        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG

    def conv_stack(self, epochs):
        return conv_stack(self, epochs)
        
