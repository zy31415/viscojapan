from os.path import exists

from .epochal_data import EpochalDataBase, EpochalData

class EpochalIncrSlip(EpochalDataBase):
    ''' Note that no time interpolation in this class.
'''
    def __init__(self, file_incr_slip):
        super().__init__(file_incr_slip)

class EpochalSlip(EpochalData):
    def __init__(self, file_slip):
        super().__init__(file_slip)

def slip_to_incr_slip(f_slip, f_incr_slip):
    assert exists(f_slip)
    assert not exists(f_incr_slip)
    
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

def incr_slip_to_slip(f_incr_slip, f_slip):
    assert not exists(f_slip)
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

