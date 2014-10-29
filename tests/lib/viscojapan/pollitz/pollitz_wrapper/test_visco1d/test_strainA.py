import unittest
from os.path import join

from viscojapan.pollitz.pollitz_wrapper import strainA
from viscojapan.test_utils import MyTestCase
from viscojapan.utils import delete_if_exists

class Test_Pollitz_strainA(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

        self.out_file = join(self.outs_dir, 'out_disp')
        delete_if_exists(self.out_file)

    def test(self):
        cmd = strainA(
            earth_model = join(self.share_dir,'earth.model'),
            decay_out = join(self.share_dir,'decay.out'),
            decay4_out = join(self.share_dir,'decay4.out'),
            vsph_out = join(self.share_dir,'vsph.out'),
            vtor_out = join(self.share_dir,'vtor.out'),

            file_out = self.out_file,
            file_flt = join(self.share_dir,'flt_0000'),
            file_sites = join(self.share_dir,'sites'),

            days_after = 100,

            if_skip_on_existing_output = True,
            stdout = None,
            stderr = None,
            )
        cmd.stdin_to_file(join(self.outs_dir, 'std.in'))
        cmd()

if __name__=='__main__':
    unittest.main()
    



