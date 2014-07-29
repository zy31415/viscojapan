from tempfile import mkstemp
from os.path import exists

from numpy import dot, hstack, copy

from ..epochal_data.epochal_slip import EpochalIncrSlip
from ..epochal_data.diff_ed import DiffED

def _check_shape_for_matrix_product(A,B):
    sh1 = A.shape
    sh2 = B.shape
    assert (len(sh1) == 2) and (len(sh2) == 2), "Wrong shape."
    assert sh1[1] == sh2[0], "Shape doesn't match!"

class JacobianVec(object):
    ''' This class defines the derivatives (a Jacobian vector,
which is a column of a Jacobian matrix) of a system described by
epochal data with respect a non-linear parameter at place indicated
by a slip0del parameter.

The one-dimension equivalence is derivative of a curve at certain point.

'''
    def __init__(self,
                 dG,
                 f_incr_slip0):
        '''
Arguments:
    dG - DiffED object.
    slip0 - incremental slip on the fault as initial value.
'''
        self.dG = dG
        self.f_incr_slip0 = f_incr_slip0
        
        assert exists(self.f_incr_slip0)

    def __call__(self, epochs):
        ''' This function returns Jacobian vector with respect to
nonlinear parameter wrt at epochs.
Return:
    Jacobian vector    
'''
        dG_stacked = self.dG.conv_stack(epochs)

        incr_slip = EpochalIncrSlip(self.f_incr_slip0)

        m_stacked = incr_slip.vstack()

        _check_shape_for_matrix_product(dG_stacked, m_stacked)
        
        jac = dot(dG_stacked,m_stacked)

        return jac

class Jacobian(object):
    def __init__(self):
        # EpochalData object of Green's functions
        #  computed with current non-linear parameters.
        self.G = None
        
        self.jacobian_vecs = []
        self.epochs = []
        
    def __call__(self):
        jacobian = []
        jacobian.append(
            self.G.conv_stack(self.epochs)
            )
        for J in self.jacobian_vecs:
            jacobian.append(J(self.epochs))

        jacobian = hstack(jacobian)
        
        return jacobian

class D_(object):
    def __init__(self):

        # Corresponding JacobianVec for each non_linear parameters
        self.jacobian_vecs = None

        # list of inital values of non_linear parameters
        self.nlin_par_values = None
        
        self.epochs = None

        # true obsevation is recorded:
        self.disp_obs = None
        # EpochalData object of observation
        self.d = None

    def __call__(self):
        self.disp_obs = self.d.vstack(self.epochs)
        d_ = copy(self.disp_obs)
        for J, val in zip(self.jacobian_vecs, self.nlin_par_values):
            d_ += (J(self.epochs)*val)
        return d_
