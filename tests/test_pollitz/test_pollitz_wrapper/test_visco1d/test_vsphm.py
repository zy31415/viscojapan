import unittest
from os.path import join

from viscojapan.pollitz.pollitz_wrapper import vsphm
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import delete_if_exists

class Test_Pollitz_vsphm(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

        self.out_file = join(self.outs_dir, 'vsph.out')
        delete_if_exists(self.out_file)

    def test(self):
        cmd = vsphm(
            earth_model = join(self.share_dir,'earth.model'),
            decay4_out = join(self.share_dir,'decay4.out'),
            vsph_out = self.out_file,
            obs_dep = 0.0,

            if_skip_on_existing_output = True,
            stdout = None,
            stderr = None)
        cmd()

if __name__=='__main__':
    unittest.main()
    



