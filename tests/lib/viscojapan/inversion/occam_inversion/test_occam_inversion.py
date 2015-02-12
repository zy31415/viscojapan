from os.path import join
import unittest

import numpy as np

import viscojapan as vj

class Test_OccamDeconvolution(vj.MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()


    def test_occam_inversion(self):
        epochs = [0, 5, 10]

        sites = [site.decode() for site in np.loadtxt(join(self.share_dir, 'sites_0462'),'4a',usecols=(0,))]

        fault_file = join(self.share_dir, 'fault_bott80km.h5')
        
        basis = vj.inv.basis.BasisMatrix.create_from_fault_file(
            fault_file, len(epochs))

        regularization = vj.inv.reg.create_roughening_temporal_regularization(
            fault_file, epochs, 1., 1.)

        inv = vj.inv.OccamDeconvolution(
            file_G0 = join(self.share_dir, 'G0_He50km_VisM6.3E18_Rake83.h5'),
            
            files_Gs = [join(self.share_dir,'G1_He50km_VisM1.0E19_Rake83.h5'),
                        join(self.share_dir,'G2_He60km_VisM6.3E18_Rake83.h5'),
                        join(self.share_dir,'G3_He50km_VisM6.3E18_Rake90.h5')
                        ],
            nlin_par_names = ['log10(visM)','log10(He)','rake'],

            file_d = join(self.share_dir, 'cumu_post_with_seafloor.h5'),
            file_sd = join(self.share_dir, 'sd_uniform.h5'),
            file_slip0 = join(self.share_dir, 'slip0.h5'),
            sites = sites,
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


    
