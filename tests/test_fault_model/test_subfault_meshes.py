import unittest
from os.path import join
import warnings

from numpy import arange, meshgrid, ascontiguousarray, linspace
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault_model.subfault_meshes import SubfaultsMeshes, \
     SubfaultsMeshesByLength, SubfaultsMeshesByNumber
from viscojapan.utils import get_this_script_dir, delete_if_exists

this_test_path = get_this_script_dir(__file__)

class TestSubFaultsMeshes(unittest.TestCase):
    def setUp(self):
        self.file_subfaults = join(this_test_path, '~test_faults.h5')
        
        self.file_gen_by_length = join(this_test_path,
                                       '~test_faults_gen_by_length.h5')

        self.file_gen_by_number = join(this_test_path,
                                       '~test_faults_gen_by_number.h5')
                
    def test_SubfaultsMeshes(self):
        delete_if_exists(self.file_subfaults)
        
        sf = SubfaultsMeshes()
        sf.x_f = linspace(0,700, 20)
        sf.y_f = linspace(0,300, 15)
        sf.save_fault_file(self.file_subfaults)

    def test_SubfaultsMeshesByLength(self):
        delete_if_exists(self.file_gen_by_length)
        
        gen = SubfaultsMeshesByLength()
        gen.subflt_sz_dip = 20.
        gen.depth_bottom_limit = 60.

        gen.flt_sz_strike_limit = 700. # km
        gen.subflt_sz_strike = 19.

        gen.save_fault_file(self.file_gen_by_length)

    def test_SubfaultsMeshesByNumber(self):
        delete_if_exists(self.file_gen_by_number)

        gen=SubfaultsMeshesByNumber()       
        
        gen.num_subflt_along_strike = 30
        gen.flt_sz_strike = 700. # km
        
        gen.num_subflt_along_dip = 20        
        gen.depth_bottom_limit = 50.

        gen.save_fault_file(self.file_gen_by_number)
        
        
        
if __name__=='__main__':
    unittest.main()
