from os.path import exists, join
import tempfile as tf
import shutil

from numpy import asarray

from .epochal_data import EpochalData
from ..utils import overrides
from .stacking import vstack_column_vec

__all__ = ['slip_to_incr_slip', 'incr_slip_to_slip',
           'interpolate_incr_slip_file',
           'EpochalSlip','EpochalIncrSlip']

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

def interpolate_incr_slip_file(in_incr_slip, epochs, out_incr_slip):
    temp_path = tf.mkdtemp(dir='/home/zy/tmp/')
    tmp1_cum_slip = join(temp_path, 'cum1.h5')
    incr_slip_to_slip(in_incr_slip, tmp1_cum_slip)

    tmp2_cum_slip = join(temp_path, 'cum2.h5')
    EpochalData(tmp1_cum_slip).respacing(epochs, tmp2_cum_slip)    
    slip_to_incr_slip(tmp2_cum_slip, out_incr_slip)
    shutil.rmtree(temp_path)    

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

    def to_cum_slip_file(self, out_file):
        incr_slip_to_slip(self.epoch_file, out_file)

    def respacing(self, epochs, out_file, delete_temp=True):
        temp_path = tf.mkdtemp(dir='/home/zy/tmp/')
        tmp1_cum_slip = join(temp_path, 'cum1.h5')
        self.to_cum_slip_file(tmp1_cum_slip)

        tmp2_cum_slip = join(temp_path, 'cum2.h5')
        EpochalData(tmp1_cum_slip).respacing(epochs, tmp2_cum_slip)    
        slip_to_incr_slip(tmp2_cum_slip, out_file)

        if delete_temp:
            shutil.rmtree(temp_path)

