import unittest
from os.path import join

from numpy import arange, asarray

import viscojapan as vj
#from viscojapan.basis_function.basis_matrix import BasisMatrix
from viscojapan.plots import MapPlotFault, plt
from viscojapan.test_utils import MyTestCase

class Test_BasisMatrix(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def plot_slip(self, slip, fn):
        mplt = MapPlotFault('/home/zy/workspace/viscojapan/inversions/static_inversion/coseismic_inversion_wider/fault_model/fault_He50km_east.h5')
        mplt.plot_slip(slip)
        plt.savefig(join(self.outs_dir,fn))
        plt.close()


    def test_gen_slip_mesh(self):                
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 20.,
            xf = arange(0,701, 20),
            dy_spline = 20.,
            yf = arange(0,221, 20),
            )

        slip = bm.gen_slip_mesh(10,0)

        self.plot_slip(slip.flatten(),'test_gen_slip_mesh.png')


    def test_gen_basis_matrix(self):
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 20.,
            xf = arange(0,701, 20),
            dy_spline = 20.,
            yf = arange(0,221, 20),
            )
        basis_mat = bm.gen_basis_matrix()

        self.plot_slip(basis_mat[:,20],'test_gen_basis_matrix.png')

    def test_gen_basis_matrix_sparse(self):
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 20.,
            xf = arange(0,701, 20),
            dy_spline = 20.,
            yf = arange(0,221, 20),
            )
        basis_mat = bm.gen_basis_matrix_sparse()

        self.plot_slip(asarray(basis_mat.todense())[:,40],
                       'test_gen_basis_matrix_sparse.png')
        

if __name__=='__main__':
    unittest.main()
