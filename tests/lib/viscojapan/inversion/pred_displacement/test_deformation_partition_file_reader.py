__author__ = 'zy'

import unittest
from os.path import join

import viscojapan as vj

class Test_DeformPartitionResultReader(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        reader = vj.inv.DeformPartitionResultReader(join(self.share_dir, 'deform_partition.h5'))
        reader.check_partition_result(join(self.share_dir,'nrough_05_naslip_11.h5'))


if __name__ == '__main__':
    unittest.main()
