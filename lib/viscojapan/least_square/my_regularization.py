from numpy import sqrt
from scipy.sparse import vstack

class Tik2SpatialTemporalReg(Regularization):
    def __init__(self):
        self.spatial_reg_row = None
        self.spatial_reg_col = None
        self.spatial_reg_row_col = None
        self.temporal_reg = None

        # wighting parameter for spatial regularization
        self.alpha = None
        
        # weighting parameter for temporal regularization
        self.beta = None
        
    def __call__(self):
        tik = vstack([self.alpha * self.spatial_reg_row(),
                self.alpha * self.spatial_reg_col(),
                sqrt(2.) * self.alpha * self.spatial_reg_row_col(),
                self.beta * self.temporal_reg()]

        return tik
                
