import numpy as np

from .epochal_file_io import EpochalFileReader
from ..utils import assert_col_vec_and_get_nrow

__all__ = ['slip_to_incr_slip', 'incr_slip_to_slip',
           'interpolate_incr_slip_file',
           'EpochalIncrSlipFileReader']

def slip_to_incr_slip(f_slip, f_incr_slip):
    assert exists(f_slip)
    
    slip = EpochalSlip(f_slip)
    epochs = slip.get_epochs()

    incr_slip = EpochalIncrSlip(f_incr_slip)

    nth = 0
    for epoch, val in slip.iter_epoch_values():
        if nth == 0:
            incr_slip.set_epoch_value(epoch, val)
            val0 = val
        else:
            incr_slip.set_epoch_value(epoch, val-val0)
            val0 = val
        nth += 1
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
    

class EpochalIncrSlipFileReader(EpochalFileReader):
    def __init__(self, epoch_file):
        super().__init__(epoch_file)

    def get_epoch_value(self, epoch):
        return self.get_epoch_value_no_interpolation(epoch)

    def get_incr_slip_at_nth_epoch(self, nth_epoch):
        return self[self.epochs[nth_epoch]]

    def get_aslip_at_nth_epoch(self,nth_epoch):
        assert nth_epoch >=0

        if nth_epoch ==0:
            return np.zeros_like(self[0])
        
        slip = self.get_incr_slip_at_nth_epoch(nth_epoch)
        
        for n in range(2,nth_epoch+1):
            slip += self.get_incr_slip_at_nth_epoch(n)
        return slip
    
    def get_cumu_slip_at_nth_epoch(self,nth_epoch):
        assert nth_epoch >=0
        slip0 = self[0]

        aslip = self.get_aslip_at_nth_epoch(nth_epoch)
        
        return slip0 + aslip

    def vstack(self):
        epochs = self.epochs
        res = self.get_epoch_value(epochs[0])
        assert_col_vec_and_get_nrow(res)
        for epoch in epochs[1:]:
            res = np.vstack((res,epoch_data.get_data_at_epoch(epoch)))
        return res
        
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
        
        
        

    
    
