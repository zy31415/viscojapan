import unittest
from os.path import join
import warnings

from numpy import arange, meshgrid, ascontiguousarray, linspace
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault_model.subfault_meshes import SubfaultsMeshes, \
     SubfaultsMeshesByLength, SubfaultsMeshesByNumber
from viscojapan.fault_model import control_points1, control_points2

from viscojapan.utils import get_this_script_dir, delete_if_exists
from viscojapan.test_utils import MyTestCase

this_test_path = get_this_script_dir(__file__)

class TestSubFaultsMeshes(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.file_subfaults = join(self.outs_dir, '~test_faults.h5')
        
        self.file_gen_by_length = join(self.outs_dir,
                                       '~test_faults_gen_by_length.h5')

        self.file_gen_by_number = join(self.outs_dir,
                                       '~test_faults_gen_by_number.h5')
                
    def test_SubfaultsMeshes(self):
        delete_if_exists(self.file_subfaults)
        
        sf = SubfaultsMeshes(control_points1)
        sf.x_f = linspace(0,700, 26)
        sf.y_f = linspace(0,300, 11)
        sf.save_fault_file(self.file_subfaults)

    def test_SubfaultsMeshesByLength(self):
        delete_if_exists(self.file_gen_by_length)
        
        gen = SubfaultsMeshesByLength(control_points2)
        gen.subflt_sz_dip = 20.
        gen.depth_bottom_limit = 60.

        gen.flt_sz_strike_limit = 700. # km
        gen.subflt_sz_strike = 19.

        gen.save_fault_file(self.file_gen_by_length)

    def test_SubfaultsMeshesByNumber(self):
        delete_if_exists(self.file_gen_by_number)

        gen=SubfaultsMeshesByNumber(control_points2)       
        
        gen.num_subflt_along_strike = 4
        gen.flt_sz_strike = 700. # km
        
        gen.num_subflt_along_dip = 3        
        gen.depth_bottom_limit = 50.

        gen.save_fault_file(self.file_gen_by_number)
        
        
        
if __name__=='__main__':
    unittest.main()
