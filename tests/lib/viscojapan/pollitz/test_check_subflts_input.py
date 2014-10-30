import unittest
from os.path import join

from viscojapan.pollitz.check_fault_input import CheckSubfaultsInput
from viscojapan.test_utils import MyTestCase

class CheckCase(MyTestCase, CheckSubfaultsInput):
    def setUp(self):
        self.this_script = __file__
        MyTestCase.setUp(self)

        self.subflts_dir = join(self.share_dir, 'subflts')
        self.original_fault_file = join(self.share_dir, 'fault.h5')

if __name__=='__main__':
    unittest.main()
    
