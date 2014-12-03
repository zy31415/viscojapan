import numpy as np
import scipy.sparse as sp

from viscojapan.fault_model import FaultFileReader
from .regularization import Leaf, Composite

__all__ = ['BoundaryRegDeadNorthAndSouth']

class _BoundaryRegularizationBase(Leaf):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__()
        self.ncols_slip = ncols_slip
        self.nrows_slip = nrows_slip

    def form_data_I_J(self):
        raise NotImplementedError()

    def generate_regularization_matrix(self):
        data, I, J, ncol = self.form_data_I_J_ncol()
        res = sp.coo_matrix(
            (data,(I,J)),
            shape = [ncol, self.ncols_slip*self.nrows_slip]
            )
        return res

    @classmethod
    def create_from_fault_file(cls, fault_file):
        fid = FaultFileReader(fault_file)        
        reg = cls(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            )
        return reg


class NorthBoundary(_BoundaryRegularizationBase):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__(ncols_slip, nrows_slip)

    def form_data_I_J_ncol(self):
        data = np.ones(self.nrows_slip)
        I = np.arange(self.nrows_slip)
        J = I * self.ncols_slip
        ncol = self.nrows_slip
        return data, I, J, ncol


class SouthBoundary(_BoundaryRegularizationBase):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__(ncols_slip, nrows_slip)

    def form_data_I_J_ncol(self):
        data = np.ones(self.nrows_slip)
        I = np.arange(self.nrows_slip)
        J = (I+1) * self.ncols_slip - 1
        ncol = self.nrows_slip
        return data, I, J, ncol


class FaultBottomBoundary(_BoundaryRegularizationBase):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__(ncols_slip, nrows_slip)
    
    def form_data_I_J_ncol(self):
        data = np.ones(self.ncols_slip)
        I = np.arange(self.ncols_slip)
        J = ((self.nrows_slip - 1) * self.ncols_slip) + \
            np.arange(self.ncols_slip)
        ncol = self.ncols_slip
        return data, I, J, ncol

class FaultTopBoundary(_BoundaryRegularizationBase):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        super().__init__(ncols_slip, nrows_slip)

    def form_data_I_J_ncol(self):
        data = np.ones(self.ncols_slip)
        I = range(self.ncols_slip)
        J = range(self.ncols_slip)
        ncol = self.ncols_slip
        return data, I, J, ncol

class DeadBoundary(Composite):
    def __init__(self,
                 ncols_slip,
                 nrows_slip
                 ):
        north = NorthBoundary(ncols_slip, nrows_slip)
        south = SouthBoundary(ncols_slip, nrows_slip)
        bott = FaultBottomBoundary(ncols_slip, nrows_slip)
        components = (north, south, bott)
        args = [1.]*3
        arg_names = ['north','south','bottom']
        super().__init__(components, args = args, arg_names = arg_names)

    @classmethod
    def create_from_fault_file(cls, fault_file):
        fid = FaultFileReader(fault_file)        
        reg = cls(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            )
        return reg

class BoundaryRegDeadNorthAndSouth(Composite):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 arg_for_dead_boundary = 1e5
                 ):
        north = NorthBoundary(ncols_slip, nrows_slip)
        south = SouthBoundary(ncols_slip, nrows_slip)
        top = FaultTopBoundary(ncols_slip, nrows_slip)

        components = (north, south, top)
        args = [arg_for_dead_boundary, arg_for_dead_boundary, 1.]
        arg_names = ['north','south','top']
        super().__init__(components, args = args, arg_names = arg_names)

    @classmethod
    def create_from_fault_file(cls, fault_file):
        fid = FaultFileReader(fault_file)        
        reg = cls(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            )
        return reg

class AllBoundaryReg(Composite):
    def __init__(self,
                 ncols_slip,
                 nrows_slip,
                 arg_for_dead_boundary = 1e5
                 ):
        dead_boundary = DeadBoundary(ncols_slip, nrows_slip)
        top = FaultTopBoundary(ncols_slip, nrows_slip)

        components = (dead_boundary, top)
        args = [arg_for_dead_boundary, 1.]
        arg_names = ['dead_boundary','top']
        super().__init__(components, args = args, arg_names = arg_names)

    @classmethod
    def create_from_fault_file(cls, fault_file):
        fid = FaultFileReader(fault_file)        
        reg = cls(
            ncols_slip = fid.num_subflt_along_strike,
            nrows_slip = fid.num_subflt_along_dip,
            )
        return reg
        
    
