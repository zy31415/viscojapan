import unittest
from os.path import join

from numpy import arange, logspace

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.static_inversion import StaticInversion
from viscojapan.test_utils import MyTestCase

class TestLeastSquare(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_StaticInversion(self):        

        fault_file = join(self.share_dir, 'fault_He50km_east.h5')

        rough = Roughening.create_from_fault_file(fault_file)
        reg = Composite().add_component(rough, 1., 'roughening')

        basis = BasisMatrix.create_from_fault_file(fault_file)

        inv = StaticInversion(
            file_G = join(self.share_dir, 'G.h5'),
            file_d = join(self.share_dir,'cumu_post_with_seafloor.h5'),
            file_sd = join(self.share_dir, 'sites_sd.h5'),
            file_sites_filter = join(self.share_dir, 'sites_with_seafloor'),
            regularization = reg,
            basis = basis,
        )

        inv.set_data_all()
        inv.run()
        inv.save(join(self.outs_dir,'out.h5'), overwrite=True)

if __name__=='__main__':
    unittest.main()
