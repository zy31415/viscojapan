from os.path import exists

from numpy import asarray

from .epochal_data import EpochalData
from ..utils import overrides
from .stacking import vstack_column_vec

# function definition

def slip_to_incr_slip(f_slip, f_incr_slip):
    assert exists(f_slip)
    
    slip = EpochalSlip(f_slip)
    epochs = slip.get_epochs()
    assert 0 in epochs, 'No zero epoch.'

    incr_slip = EpochalIncrSlip(f_incr_slip)

    for epoch, val in slip.iter_epoch_values():
        if epoch == 0:
            incr_slip.set_epoch_value(epoch, val)
            val0 = val
        else:
            incr_slip.set_epoch_value(epoch, val-val0)
            val0 = val
    incr_slip.copy_info_from(f_slip)

def incr_slip_to_slip(f_incr_slip, f_slip):
    assert exists(f_incr_slip)

    incr_slip = EpochalIncrSlip(f_incr_slip)
    epochs = incr_slip.get_epochs()
    assert 0 in epochs, 'No zero epoch.'

    slip = EpochalSlip(f_slip)
    
    for epoch, val in incr_slip.iter_epoch_values():
        if epoch == 0:
            val0 = val
        else:
            val0 += val
        slip.set_epoch_value(epoch, val0)

    slip.copy_info_from(f_incr_slip)

# classes definition

class EpochalSlip(EpochalData):
    def __init__(self, file_slip):
        super().__init__(file_slip)

    def get_slip_at_subflt(self, irow, icol):
        epochs = self.get_epochs()
        ys = []
        for epoch in epochs:
            slip = self.get_epoch_value(epoch)
            ys.append(slip[irow, icol])
        return asarray(ys,float)

class EpochalIncrSlip(EpochalSlip):
    ''' Note that no time interpolation in this class.
'''
    def __init__(self, file_incr_slip):
        super().__init__(file_incr_slip)

    @overrides(EpochalSlip)
    def get_epoch_value(self, epoch):
        return self._get_epoch_value(epoch)

    def vstack(self):
        epochs = self.get_epochs()
        return vstack_column_vec(self, epochs)

