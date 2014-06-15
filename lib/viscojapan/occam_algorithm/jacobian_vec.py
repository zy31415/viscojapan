from tempfile import mkstemp
from os.path import exists

from numpy import dot

from ..epochal_data.epochal_slip import slip_to_incr_slip, EpochalIncrSlip
from ..epochal_data.diff_ed import DiffED
from .stacking import vstack_column_vec, conv_stack

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
    def __init__(self, dG, f_slip0):
        '''
Arguments:
    dG - DiffED object.
    slip0 - slip on the fault as initial value.
'''
        self.dG = dG
        self.f_slip0 = f_slip0
        assert exists(self.f_slip0)

    def __call__(self, epochs):
        ''' This function returns Jacobian vector with respect to
nonlinear parameter wrt at epochs.
Return:
    Jacobian vector    
'''
        dG_stacked = conv_stack(self.dG, epochs)

        fid, f_incr_slip = mkstemp(dir='/home/zy/tmp/')
        slip_to_incr_slip(self.f_slip0,f_incr_slip)

        incr_slip = EpochalIncrSlip(f_incr_slip)

        m_stacked = vstack_column_vec(incr_slip, epochs)

        _check_shape_for_matrix_product(dG_stacked, m_stacked)
        
        jac = dot(dG_stacked,m_stacked)

        return jac
        
        
        
    
