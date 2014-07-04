import unittest
from os.path import join

from viscojapan.pollitz.gen_subflts_input import \
     gen_subflts_input_for_pollitz
from viscojapan.utils import get_this_script_dir
from viscojapan.test_utils import MyTestCase

class Test_gen_subflts_input_for_pollitz(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        gen_subflts_input_for_pollitz(join(self.share_dir, 'fault.h5'), '~outs/subflts/')

if __name__ == '__main__':
    unittest.main()
