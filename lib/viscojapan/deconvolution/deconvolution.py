class Deconvolution(object):
    def __init__(self):
        self.epochs = None

    def _init_tikhonov_regularization(self):
        # regularization
        tik = TikhonovSecondOrder()
        tik.nrows_slip = 10
        tik.ncols_slip = 25
        tik.row_norm_length = 1
        tik.col_norm_length = 28./23.03
        tik.num_epochs = len(self.epochs)
        tik.num_nlin_pars = 0
        self.tikhonov_regularization = tik
        
