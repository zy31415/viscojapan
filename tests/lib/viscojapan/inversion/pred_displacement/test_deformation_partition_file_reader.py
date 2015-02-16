__author__ = 'zy'

import unittest
from os.path import join

import viscojapan as vj

class Test_DeformPartitionResultReader(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        reader = vj.inv.DeformPartitionResultReader('/home/zy/workspace/viscojapan/tests/share/deformation_partition.h5')
        reader.check_partition_result('/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5')


if __name__ == '__main__':
    unittest.main()
