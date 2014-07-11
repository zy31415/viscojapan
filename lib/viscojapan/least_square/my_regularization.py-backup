from numpy import sqrt, asarray
from numpy.linalg import norm
from scipy.sparse import vstack

from .regularization import Regularization, \
     RowRoughening, ColRoughening, RowColRoughening,\
     TemporalRegularization
from ..utils import overrides, _assert_column_vector

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

    def get_spatial_roughness_matrix(self):
        row_reg = self._compute_row_reg_mat()
        col_reg = self._compute_col_reg_mat()
        row_col_reg = self._compute_row_col_reg_mat()
        
        res = vstack([row_reg, col_reg, sqrt(2) * row_col_reg])
        
        return res

    def get_temporal_roughness_matrix(self):
        reg = TemporalRegularization()
        reg.epochs = self.epochs
        reg.num_subflts = self.num_subfaults()
        reg.num_nlin_pars = self.num_nlin_pars
        return reg()        
    
    def get_wighted_spatial_temporal_roughness_matrix(self, alpha, beta):
        spatial_reg = self.get_spatial_roughness_matrix()

        if len(self.epochs) >= 3:
            time_reg = self.get_temporal_roughness_matrix()
            res = vstack([alpha * spatial_reg, beta * time_reg])
        else:
            res = alpha * spatial_reg
        return res        

    @overrides(Regularization)
    def __call__(self, alpha, beta):
        res = self.get_wighted_spatial_temporal_roughness_matrix(alpha, beta)
        return res
    
    def get_spatial_roughness(self, m):
        _assert_column_vector(m)
        roughness_mat = self.get_spatial_roughness_matrix()
        rough = norm(asarray(roughness_mat.dot(m), float))
        return float(rough)

    def get_temporal_roughness(self, m):
        _assert_column_vector(m)
        roughness_mat = self.get_temporal_roughness_matrix()
        rough = norm(asarray(roughness_mat.dot(m), float))
        return float(rough)
    
        

        
        
        
                
