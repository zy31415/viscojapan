import unittest
from os.path import join

from viscojapan.pollitz.parse_fault_input import parse_fault_input
from viscojapan.test_utils import MyTestCase

class Test_parse_fault_input(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        
    def test(self):
        res = parse_fault_input(join(self.share_dir, 'fault.in2'))
        print(res)

if __name__=='__main__':
    unittest.main()
                    
