import h5py 

class DiffED(object):
    ''' This class computes the diffretial of two EpochData objects
with respcet to (wrt) the change of an indicated variable.
'''
    def __init__(self, obj1_epoch_data, obj2_epoch_data, wrt):
        ''' Arguments:
obj1_epoch_data : object of EpochalData
obj2_epoch_data : object of EpochalData
wrt - with respect to, variable that the change WRT.
'''
        self.obj1_epoch_data = obj1_epoch_data
        self.obj2_epoch_data = obj2_epoch_data
        self.wrt = wrt

        self._init()
        
    def _init(self):
        assert self.obj1_epoch_data.has_info(self.wrt)
        assert self.obj2_epoch_data.has_info(self.wrt)
        
        self._get_vars()

    def _get_vars(self):
        self.var1 = float(self.obj1_epoch_data.get_info(self.wrt))
        setattr(self, self.wrt+'1', self.var1)

        self.var2 = float(self.obj2_epoch_data.get_info(self.wrt))
        setattr(self, self.wrt+'2', self.var2)

    def get_epoch_value(self, day):
        G1 = self.obj1_epoch_data.get_epoch_value(day)
        G2 = self.obj2_epoch_data.get_epoch_value(day)

        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG
        
