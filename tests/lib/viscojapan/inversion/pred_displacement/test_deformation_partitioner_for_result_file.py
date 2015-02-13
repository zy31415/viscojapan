__author__ = 'zy'

import unittest
from os.path import join

import viscojapan as vj

class Test_DeformPartitionerForResultFile(vj.test_utils.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test1(self):
        res_file = '/home/zy/workspace/viscojapan/tests/share/nrough_05_naslip_11.h5'
        sites_for_prediction = ['J550']

        pred = vj.inv.DeformPartitionerForResultFile(
            result_file = res_file,
            file_G0 = '/home/zy/workspace/viscojapan/tests/share/G0_He50km_VisM6.3E18_Rake83.h5',
            files_Gs = ['/home/zy/workspace/viscojapan/tests/share/G1_He50km_VisM1.0E19_Rake83.h5',
                        '/home/zy/workspace/viscojapan/tests/share/G2_He60km_VisM6.3E18_Rake83.h5',
                        '/home/zy/workspace/viscojapan/tests/share/G3_He50km_VisM6.3E18_Rake90.h5'
                        ],
            file_slip0 = '/home/zy/workspace/viscojapan/tests/share/slip0.h5',
            sites_for_prediction = sites_for_prediction
        )

        disp = pred.E_co()
        disp = pred.E_aslip(10)
        disp = pred.R_nth_epoch(3, 500)
        disp = pred.R_co(500)
        disp = pred.R_aslip(500)

        pred.save(join(self.outs_dir, 'partition_from_result_file.h5'))

if __name__ == '__main__':
    unittest.main()
