import unittest
from os.path import join

from viscojapan.pollitz.gen_subflts_input import \
     gen_subflts_input
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_gen_subflts_input(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        gen_subflts_input(
            join(self.share_dir, 'fault.h5'),
            '~outs/subflts/',
            rake = 80.)

    def test2(self):
        gen_subflts_input(
            join(self.share_dir, 'fault.h5'),
            '~outs/subflts/',
            rake = 80., slip = [1,2,3,4,5,6,7,8])

if __name__ == '__main__':
    unittest.main()
