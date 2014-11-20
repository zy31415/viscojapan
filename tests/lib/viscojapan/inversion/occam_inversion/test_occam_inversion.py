from os.path import join
import os
import unittest

from viscojapan.inversion import OccamDeconvolution
from viscojapan.utils import delete_if_exists, get_this_script_dir
from viscojapan.test_utils import MyTestCase
from viscojapan.inversion.regularization import\
     create_roughening_temporal_regularization
from viscojapan.inversion.basis_function import BasisMatrix

class TestOccamDeconvolution(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test_occam_inversion(self):
        epochs = [0, 5, 10]
        fault_file = join(self.share_dir, 'fault_bott60km.h5')
        
        basis = BasisMatrix.create_from_fault_file(
            fault_file, len(epochs))

        regularization = create_roughening_temporal_regularization(
            fault_file, epochs, 1., 1.)

        inv = OccamDeconvolution(
            file_G0 = join(self.share_dir, 'G0_He50km_VisM6.3E18_Rake83.h5'),
            
            files_Gs = [join(self.share_dir,'G1_He50km_VisM1.0E19_Rake83.h5'),
                        join(self.share_dir,'G2_He40km_VisM6.3E18_Rake83.h5'),
                        join(self.share_dir,'G3_He50km_VisM6.3E18_Rake90.h5')
                        ],
            nlin_par_names = ['log10(visM)','log10(He)','rake'],

            file_d = join(self.share_dir, 'cumu_post_with_seafloor.h5'),
            file_sd = join(self.share_dir, 'sites_sd.h5'),
            file_incr_slip0 = join(self.share_dir, 'slip0.h5'),
            filter_sites_file = join(self.share_dir, 'sites_0462'),
            epochs = epochs,
            regularization = regularization,
            basis = basis,          
            )

        inv.set_data_all()
        inv.invert()
        inv.predict()
        inv.save(join(self.outs_dir,'out.h5'), overwrite=True)
        

if __name__ == '__main__':
    unittest.main()


    
