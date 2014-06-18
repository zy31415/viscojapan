from ..least_square import LeastSquareTik2

class StaticInversionTik2(LeastSquareTik2):
    def __init__(self):
        super().__init__()
        self.num_epochs = 1
        self.num_nlin_pars = 0
        
        
