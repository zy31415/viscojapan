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
        jacobian_nonlin = self.non_lin_JacobianVecs[0]()
        for J in self.non_lin_JacobianVecs[1:]:
            jacobian_nonlin = hstack(jacobian_nonlin,J())
        G_stacked = conv_stack(self.G, self.epochs)
        jacobian = hstack(G_stacked, jacobian_nonlin)
        return Jacobian

    def d_(self):
        d_ = vstack_colum_vec(self.d)
        for J, val in zip(self.non_lin_JacobianVecs, self.non_lin_par_vals):
            d_ += J*val
        return d_
    
