from numpy import hstack

from .stacking import vstack_column_vec, conv_stack

class FormulatOccam(object):
    ''' This class prpare matrix Jac and vector d_ for O
ccam nonlinear inversion.
'''
    def __init__(self):

        # epochs used in inversion.
        self.epochs = []
        
        # list of inital values of non_linear parameters
        self.non_lin_par_vals = []

        # Corresponding JacobianVec for each non_linear parameters
        self.non_lin_JacobianVecs = []

        # EpochalData object of Green's functions
        #  computed with current non-linear parameters.
        self.G = None

        # EpochalData object of observation
        self.d = None

    def Jacobian(self):
        jac_nl = self.non_lin_JacobianVecs[0](self.epochs)
        for J in self.non_lin_JacobianVecs[1:]:
            jac_nl = hstack((jac_nl, J(self.epochs)))
            
        G_stacked = conv_stack(self.G, self.epochs)
        
        jacobian = hstack((G_stacked, jac_nl))
        
        return jacobian

    def d_(self):
        d_ = vstack_column_vec(self.d, self.epochs)
        for J, val in zip(self.non_lin_JacobianVecs, self.non_lin_par_vals):
            d_ += (J(self.epochs)*val)
        return d_
    
