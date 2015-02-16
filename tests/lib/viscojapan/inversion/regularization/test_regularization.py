import unittest
from os.path import join

from pylab import plt
from numpy import asarray

import viscojapan as vj

from viscojapan.inversion.regularization.roughening import \
     RowRoughening, ColRoughening, RowColRoughening

from viscojapan.inversion.regularization.expand_for_epochs import ExpandForAllEpochs

from viscojapan.test_utils import MyTestCase

class Test_Regularization(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()
        self.fault_file = '/home/zy/workspace/viscojapan/tests/share/fault_bott80km.h5'

    def plot_mat(self, mat, fn):
        plt.matshow(asarray(mat.todense()))
        plt.axis('equal')
        sh = mat.shape
        plt.gca().set_yticks(range(0,sh[0]))
        plt.gca().set_xticks(range(0,sh[1]))
        plt.grid('on')
        plt.colorbar()
        plt.savefig(join(self.outs_dir, fn))
        plt.close()
        
    def test_row_roughening(self):
        reg = RowRoughening(
            ncols_slip = 5,
            nrows_slip = 3
            )
        reg_mat = reg()
        #print(reg_mat.todense())
        self.plot_mat(reg_mat, 'row_roughening_mat.png')

    def test_col_roughening(self):
        reg = ColRoughening(
            ncols_slip = 5,
            nrows_slip = 3
            )
        reg_mat = reg()
        #print(reg_mat.todense())
        self.plot_mat(reg_mat, 'col_roughening_mat.png')

    def test_RowColRoughening(self):
        reg = RowColRoughening(
            ncols_slip = 5,
            nrows_slip = 3
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'row_col_roughening_mat.png')

    def test_roughening(self):
        reg = vj.inv.reg.Roughening(
            ncols_slip = 5,
            nrows_slip = 4,
            norm_length_strike = 1,
            norm_length_dip = 1,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'roughening_mat.png')

    def test_ExpandForAllEpochs(self):
        reg = vj.inv.reg.Roughening(
            ncols_slip = 5,
            nrows_slip = 4,
            norm_length_strike = 1,
            norm_length_dip = 1,
            )
        
        expanded_reg = ExpandForAllEpochs(
            reg = reg,
            num_epochs = 3)

        reg_mat = expanded_reg()
        self.plot_mat(reg_mat, 'expanded_for_all.png')

    def test_TemporalRegularization(self):
        reg = vj.inv.reg.TemporalRegularization(
            num_subflts = 4,
            epochs = [1, 2, 5]
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'temporal_reg_mat.png')

    def test_create_roughening_temporal_regularization(self):
        epochs = [0, 2, 5]
        rough = 1.0
        temp = 10.
        reg = vj.inv.reg.create_roughening_temporal_regularization(
            self.fault_file, epochs, rough, temp)
        reg_mat = reg()
        self.plot_mat(reg_mat, 'roughening_temporal.png')


    def test_NorthBoundary(self):
        reg = vj.inv.reg.NorthBoundary(
            ncols_slip = 5,
            nrows_slip = 4,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'north_boundary.png')

    def test_SouthBoundary(self):
        reg = vj.inv.reg.SouthBoundary(
            ncols_slip = 5,
            nrows_slip = 4,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'south_boundary.png')

    def test_FaultBottomBoundary(self):
        reg = vj.inv.reg.FaultBottomBoundary(
            ncols_slip = 5,
            nrows_slip = 4,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'bottom_boundary.png')

    def test_FaultTopBoundary(self):
        reg = vj.inv.reg.FaultTopBoundary(
            ncols_slip = 5,
            nrows_slip = 4,
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'top_boundary.png')

    def test_FaultTopBoundary_create_from_fault_file(self):
        reg = vj.inv.reg.FaultTopBoundary.create_from_fault_file(self.fault_file)
        reg_mat = reg()
        self.plot_mat(reg_mat, 'top_boundary_gen_from_file.png')

    def test_DeadBoundary(self):
        reg = vj.inv.reg.DeadBoundary(
        ncols_slip = 5,
        nrows_slip = 4,
        )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'dead_boundary.png')

    def test_AllBoundaryReg(self):
        reg = vj.inv.reg.AllBoundaryReg(
            ncols_slip = 5,
            nrows_slip = 4,
            arg_for_dead_boundary = 10
            )
        reg_mat = reg()
        self.plot_mat(reg_mat, 'all_boundary.png')

    def test_AllBoundaryReg_create_from_fault_file(self):
        reg = vj.inv.reg.AllBoundaryReg.create_from_fault_file(self.fault_file)
        reg_mat = reg()
        self.plot_mat(reg_mat, 'all_boundary_gen_from_file.png')
        
        
if __name__ == '__main__':
    unittest.main()
