import unittest
from os.path import join

from viscojapan.pollitz.pollitz_wrapper.utils import read_flt_file_for_stdin
from viscojapan.test_utils import MyTestCase

class Test_test_utils(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        head = read_flt_file_for_stdin(join(self.share_dir, 'flt_0000'),'head')
        body = read_flt_file_for_stdin(join(self.share_dir, 'flt_0000'),'body')
        whole = read_flt_file_for_stdin(join(self.share_dir, 'flt_0000'),'whole')

if __name__ == '__main__':
    unittest.main()
