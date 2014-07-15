from scipy.sparse import eye

from .regularization import Regularization

class Intensity(Regularization):
    def __init__(self,
                 num_pars
                 ):
        self.num_pars = num_pars
        
    def generate_regularization_matrix(self):        
        return eye(self.num_pars)
