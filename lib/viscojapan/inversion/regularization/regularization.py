''' Composite Pattern
'''
from numpy import dot
import scipy.sparse as sparse

def vstack_reg_mat(reg_mats, reg_pars):
    assert len(reg_mats) == len(reg_pars)
    L_list = []
    for L, arg in zip(reg_mats, reg_pars):
        tp = sparse.csr_matrix(L)
        L_list.append(arg*tp)
    L_stack = sparse.vstack(L_list)
    return L_stack

class Regularization(object):        
    def __call__(self):
        return self.generate_regularization_matrix()        

    def generate_regularization_matrix(self):
        raise NotImplementedError(
            "This interface returns the regularization matrix.")

    def reg_vec(self, m):
        return self().dot(m)

    def solution_norm(self, m):
        tp = self().dot(m)
        res = dot(tp.T,tp)[0,0]
        return res

        
class Leaf(Regularization):
    def generate_regularization_matrix(self):
        raise NotImplementedError(
                "This interface returns the regularization matrix.")

class Composite(Regularization):
    def __init__(self,
                 components = None,
                 args = None,
                 arg_names = None):
        if components is None:
            self.components = []
        else:
            self.components = components

        if args is None:
            self.args = []
        else:
            self.args = args

        if arg_names is None:
            self.arg_names = []
        else:
            self.arg_names = arg_names
        
    def generate_regularization_matrix(self):
        mats = []
        for reg in self.components:
            mats.append(reg.generate_regularization_matrix())
        L = vstack_reg_mat(mats, self.args)
        return L

    def components_solution_norms(self,m):    
        res = []
        for reg in self.components:
            tp = reg.solution_norm(m)
            res.append(tp)
        return res

    def add_component(self, component, arg=1., arg_name=None):
        self.components.append(component)
        self.args.append(arg)
        self.arg_names.append(arg_name)
        return self

    def update_args(self,args):
        assert len(args) == self.args
        self.args = args
        return self
        
        
        
    
