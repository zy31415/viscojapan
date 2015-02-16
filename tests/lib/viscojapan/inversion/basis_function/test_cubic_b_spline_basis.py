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
        fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5'
        mplt = MapPlotFault(fault_file)
        mplt.plot_slip(slip)
        plt.savefig(join(self.outs_dir,fn))
        plt.close()


    def test_gen_slip_mesh(self):                
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 25.,
            xf = arange(0,701, 25),
            dy_spline = 25.,
            yf = arange(0,301, 25),
            )

        slip = bm.gen_slip_mesh(10,0)

        self.plot_slip(slip.flatten(),'test_gen_slip_mesh.png')


    def test_gen_basis_matrix(self):
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 25.,
            xf = arange(0,701, 25),
            dy_spline = 25.,
            yf = arange(0,301, 25),
            )
        basis_mat = bm.gen_basis_matrix()

        self.plot_slip(basis_mat.toarray()[:,25],'test_gen_basis_matrix.png')

    def test_gen_basis_matrix_sparse(self):
        bm = vj.inv.basis.BasisMatrixBSpline(
            dx_spline = 25.,
            xf = arange(0,701, 25),
            dy_spline = 25.,
            yf = arange(0,301, 25),
            )
        basis_mat = bm.gen_basis_matrix_sparse()

        self.plot_slip(asarray(basis_mat.todense())[:,40],
                       'test_gen_basis_matrix_sparse.png')
        

if __name__=='__main__':
    unittest.main()
