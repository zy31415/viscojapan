import unittest
import os
from os.path import join

from numpy import ones

from viscojapan.epochal_data.stacking import break_col_vec_into_epoch_file,\
     break_m_into_incr_slip_file, break_m_into_slip_file
from viscojapan.utils import delete_if_exists, get_this_script_dir

this_test_dir = get_this_script_dir(__file__)

class TestBreakColVecIntoEpochFile(unittest.TestCase):
    def setUp(self):
        vec = ones(100).reshape([-1,1])
        for nth in range(10):
            vec[nth*10:(nth+1)*10,0] = nth

        self.vec = vec
        self.epochs = range(0,10)

        self.h5_file_name = join(this_test_dir, 'break_into_test.h5')        
        delete_if_exists(self.h5_file_name)

    def test_basic(self):
        break_col_vec_into_epoch_file(self.vec, self.epochs, self.h5_file_name)

    def test_consistency_check1(self):
        break_col_vec_into_epoch_file(self.vec, self.epochs, self.h5_file_name,
                                      rows_per_epoch=10)
##
    def test_consistency_check2(self):
        with self.assertRaises(AssertionError) as cm:
            break_col_vec_into_epoch_file(
                self.vec, self.epochs, self.h5_file_name,
                rows_per_epoch=11)
        print(cm.exception)
##
    def test_info_set(self):
        info_dic={'A':'a',
                  'B':'b',
                  'C':'c'}
        break_col_vec_into_epoch_file(self.vec, self.epochs, self.h5_file_name,
                                      rows_per_epoch=10, info_dic = info_dic)

    def test_break_m_into_incr_slip_file(self):
        incr_slip_fn = join(this_test_dir, 'break_into_incr_slip.h5')        
        delete_if_exists(incr_slip_fn)
        
        break_m_into_incr_slip_file(self.vec, self.epochs, incr_slip_fn,
                                      rows_per_epoch=10)

    def test_break_m_into_slip_file(self):    
        slip_fn = join(this_test_dir, 'break_into_slip.h5')        
        delete_if_exists(slip_fn)
        break_m_into_slip_file(self.vec, self.epochs, slip_fn,
                               rows_per_epoch=10)

if __name__ == '__main__':
    unittest.main()
                                      
