import unittest
from os.path import join
import warnings

from numpy import arange, meshgrid, ascontiguousarray, linspace
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault.subfault_meshes import SubfaultsMeshes
from viscojapan.utils import get_this_script_dir, delete_if_exists

this_test_path = get_this_script_dir(__file__)

class TestSubFaultsMeshes(unittest.TestCase):
    def setUp(self):
        self.file_subfaults = join(this_test_path, '~test_subfaults.h5')
        delete_if_exists(self.file_subfaults)

    def test(self):
        sf = SubfaultsMeshes()
        sf.num_subflt_along_strike = 26
        sf.num_subflt_along_dip = 16
        sf.depth_limit = 60

        sf.save_fault_file(self.file_subfaults)

if __name__=='__main__':
    unittest.main()
