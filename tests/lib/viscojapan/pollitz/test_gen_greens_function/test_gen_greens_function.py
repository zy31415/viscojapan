import unittest
from os.path import join
import glob

from viscojapan.test_utils import MyTestCase
from viscojapan.pollitz.compute_greens_function \
     import ComputeGreensFunction
from viscojapan.utils import delete_if_exists

class Test_ComputeGreensFunction(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.out1 = join(self.outs_dir,'out1')
        delete_if_exists(self.out1)
        
        self.out2 = join(self.outs_dir,'out2')

## These tests use dpool, which need to be redesined.
        

##    def test(self):
##        subflts_files = \
##            sorted(glob.glob(join(self.share_dir, 'subflts/','flt_????')))
##        com = ComputeGreensFunction(
##            epochs = [0, 1],
##            file_sites = join(self.share_dir, 'sites'),
##            earth_file = join(self.share_dir, 'earth.model'),
##            earth_file_dir =  join(self.share_dir, 'earth_files/'),
##            outputs_dir = self.out1,
##            subflts_files = subflts_files,
##            controller_file =  join(self.share_dir,'pool.config'),
##            )
##        com.run()
##
##    def test_skip(self):
##        subflts_files = \
##            sorted(glob.glob(join(self.share_dir, 'subflts/','flt_????')))
##        com = ComputeGreensFunction(
##            epochs = [0, 1],
##            file_sites = join(self.share_dir, 'sites'),
##            earth_file = join(self.share_dir, 'earth.model'),
##            earth_file_dir =  join(self.share_dir, 'earth_files/'),
##            outputs_dir = self.out2,
##            subflts_files = subflts_files,
##            controller_file =  join(self.share_dir,'pool.config'),
##            )
##        com.run()
##        com.gen_epochal_file()


if __name__ == '__main__':
    unittest.main()
