import unittest

from viscojapan.pollitz.check_fault_input import CheckSubfaultsInput
from viscojapan.test_utils import MyTestCase

class CheckCase(MyTestCase, CheckSubfaultsInput):
    def setUp(self):
        self.subflts_dir = 'subflts'
        self.original_fault_file = 'fault.h5'

        self.this_script = __file__
        MyTestCase.setUp(self)

if __name__=='__main__':
    unittest.main()
    
