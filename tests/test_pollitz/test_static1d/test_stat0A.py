import unittest
from os.path import join

from viscojapan.pollitz.stat0A import stat0A
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import delete_if_exists

class Test_Pollitz_stat0A(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

        self.out_file = join(self.outs_dir, 'stat0.out')
        delete_if_exists(self.out_file)

    def test(self):
        cmd = stat0A(
            earth_model_stat = join(self.share_dir,'earth.model'),
            stat0_out = self.out_file,
            l_min = 1,
            l_max = 10,
            fault_bottom_depth = 60.,
            fault_top_depth = 3.,
            obs_dep = 0.,
            output_dir = '.',
            if_skip_on_existing_output = True,
            stdout = None,
            stderr = None)
        cmd()

if __name__=='__main__':
    unittest.main()
    



