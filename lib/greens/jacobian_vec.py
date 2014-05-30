from numpy import dot

from .diff_ed import DiffED
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
by a model parameter.

The one-dimension equivalence is derivative of a curve at certain point.

'''
    def __init__(self, dG, m0):
        '''
Arguments:
    dG - DiffED object.
    m0 - EpochalData object.
        linear model parameter, incremental slip
         on the fault.
'''
        self.dG = dG
        self.m0 = m0    

    def __call__(self, epochs):
        ''' This function returns Jacobian vector with respect to
nonlinear parameter wrt at epochs.
Return:
    Jacobian vector    
'''
        dG_stacked = conv_stack(self.dG, epochs)
        m_stacked = vstack_column_vec(self.m0, epochs)

        _check_shape_for_matrix_product(dG_stacked, m_stacked)
        
        print("    Caution: Large matrix-vecto product.")
        jac = dot(dG_stacked,m_stacked)

        return jac
        
        
        
    
