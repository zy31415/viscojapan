import numpy as np
import scipy.sparse as sp

from viscojapan.fault_model import FaultFileIO
from .regularization import Leaf, Composite

class PunishEdge(Leaf):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__()
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip

    def norm_edge(self):
        data = np.ones(self.ncols_slip)
        I = range(self.ncols_slip)
        J = range(self.ncols_slip)
        res = sp.coo_matrix(
            (data,(I,J)),
            shape = [self.ncols_slip, self.ncols_slip*self.nrows_slip]
            )
        return res

    def generate_regularization_matrix(self):
        return self.norm_edge()

    @staticmethod
    def create_from_fault_file(fault_file):
        fid = FaultFileIO(fault_file)
        
        L2 = PunishEdge(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            )
        return L2
        
    
        
        
    
