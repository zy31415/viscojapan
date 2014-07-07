import unittest
from os.path import join

from viscojapan.pollitz.pollitz_wrapper import stat2gA
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import delete_if_exists

class Test_Pollitz_stat2gA(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

        self.out_file = join(self.outs_dir, 'out_disp')
        delete_if_exists(self.out_file)

    def test(self):
        cmd = stat2gA(
            earth_model_stat = join(self.share_dir,'earth.model'),
            stat0_out = join(self.share_dir,'stat0.out'),
            file_flt = join(self.share_dir,'flt_0000'),
            file_sites = join(self.share_dir,'stations.in'),
            file_out = self.out_file,
            if_skip_on_existing_output = True,
            stdout = None,
            stderr = None)
        cmd()

if __name__=='__main__':
    unittest.main()
    



