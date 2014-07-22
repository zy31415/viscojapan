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
        fault_file = join(self.share_dir, 'fault_He50km.h5')
        
        basis = BasisMatrix.create_from_fault_file(
            fault_file, len(epochs))

        regularization = create_roughening_temporal_regularization(
            fault_file, epochs, 1., 1.)
        
        inv = OccamDeconvolution(
            file_G0 = join(self.share_dir,'G_He50km_Vis5.8E18_Rake90.h5'),
            files_Gs = [join(self.share_dir,'G_He55km_Vis5.8E18_Rake90.h5'),
                        join(self.share_dir,'G_He50km_Vis5.8E18_Rake95.h5')],
            nlin_par_initial_values = [50.,90.],
            nlin_par_names = ['He','rake'],
            file_d = join(self.share_dir, 'cumu_post_with_seafloor.h5'),
            file_sd = join(self.share_dir, 'sites_sd.h5'),
            file_incr_slip0 = join(self.share_dir, 'incr_slip0.h5'),
            filter_sites_file = join(self.share_dir, 'sites_0093'),
            epochs = epochs,
            regularization = regularization,
            basis = basis,          
            )
        inv.set_data_all()
        inv.invert()
        inv.predict()
        

if __name__ == '__main__':
    unittest.main()


    
