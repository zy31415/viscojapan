from scipy import sparse

from .regularization import Leaf

__all__ = ['ExpandForAllEpochs','ExpandForOnlyFirstEpoch',
           'ExpandExceptFirstEpoch','ExpandForCumulativeSlip']

def stack_to_lower_tri(mat, size):
    out = []
    for i in range(size):
        tp = []
        for j in range(size):
            if j>i:
                tp.append(None)
            else:
                tp.append(mat)
        out.append(tp)
    return out    

class ExpandForAllEpochs(Leaf):
    def __init__(self,
                 reg,
                 num_epochs):
        self.reg = reg
        self.num_epochs = num_epochs

    def generate_regularization_matrix(self):
        regmat = self.reg()
        L = sparse.block_diag([regmat]*self.num_epochs)
        return L

class ExpandForOnlyFirstEpoch(Leaf):
    def __init__(self,
                 reg,
                 num_epochs):
        self.reg = reg
        self.num_epochs = num_epochs

    def generate_regularization_matrix(self):
        regmat = self.reg()
        shape = regmat.shape
        shape = (shape[0]*(self.num_epochs-1), shape[1]*(self.num_epochs-1))
        zero = sparse.csc_matrix(shape)
        L = sparse.block_diag([regmat, zero])
        return L        
        
class ExpandExceptFirstEpoch(Leaf):
    def __init__(self,
                 reg,
                 num_epochs):
        self.reg = reg
        self.num_epochs = num_epochs

    def generate_regularization_matrix(self):
        regmat = self.reg()
        shape = regmat.shape
        zero = sparse.csc_matrix(shape)
        L = sparse.block_diag([zero]+[regmat]*(self.num_epochs-1))
        return L  

class ExpandForCumulativeSlip(Leaf):
    def __init__(self,
                 reg,
                 num_epochs):
        self.reg = reg
        self.num_epochs = num_epochs

    def generate_regularization_matrix(self):
        regmat = self.reg()
        tp = stack_to_lower_tri(regmat, self.num_epochs)
        L = sparse.bmat(tp)
        return L
