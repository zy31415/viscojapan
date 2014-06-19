from numpy import sqrt
from scipy.sparse import vstack

from .regularization import Regularization, \
     RowRoughening, ColRoughening, RowColRoughening,\
     TemporalRegularization
from ..utils import overrides


class SpatialTemporalReg(Regularization):
    def __init__(self):
        self.epochs = None

        # spatical geometry
        self.nrows_slip = None
        self.ncols_slip = None
        self.row_norm_length = 1.
        self.col_norm_length = 28./23.03

        self.num_nlin_pars = None


    def num_epochs(self):
        return len(self.epochs)

    def num_subfaults(self):
        return self.nrows_slip * self.ncols_slip 

    def _init_spatial_regularization_class(self, reg):
        reg.nrows_slip = self.nrows_slip
        reg.ncols_slip = self.ncols_slip
        reg.row_norm_length = self.row_norm_length 
        reg.col_norm_length = self.col_norm_length

        reg.num_epochs = self.num_epochs()
        reg.num_nlin_pars = self.num_nlin_pars

    def _compute_row_reg_mat(self):
        reg = RowRoughening()
        self._init_spatial_regularization_class(reg)
        return reg()

    def _compute_col_reg_mat(self):
        reg = ColRoughening()
        self._init_spatial_regularization_class(reg)
        return reg()

    def _compute_row_col_reg_mat(self):
        reg = RowColRoughening()
        self._init_spatial_regularization_class(reg)
        return reg()

    def _compute_time_reg_mat(self):
        reg = TemporalRegularization()
        reg.epochs = self.epochs
        reg.num_subflts = self.num_subfaults()
        reg.num_nlin_pars = self.num_nlin_pars

        return reg()        
    
    def _compute_final_reg_mat(self, alpha, beta):
        row_reg = self._compute_row_reg_mat()
        col_reg = self._compute_col_reg_mat()
        row_col_reg = self._compute_row_col_reg_mat()
        time_reg = self._compute_time_reg_mat()

        res = vstack([alpha * row_reg,
               alpha * col_reg,
               alpha * sqrt(2) * row_col_reg,
               beta * time_reg])
        return res
        

    @overrides(Regularization)
    def __call__(self, alpha, beta):
        res = self._compute_final_reg_mat(alpha, beta)
        return res
                
