from viscojapan.epochal_data import EpochalG, EpochalDisplacement, EpochalDisplacementSD
from viscojapan.inversion.least_square import LeastSquareWithRegularization


class StaticInversion(object):
    def __init__(self,
                 G_file,
                 obs_file,
                 sd_file,
                 sites_filter_file,
                 basis_mat,
                 reg_mats,
                 reg_pars,
                 reg_par_names,
                 output_file,
                 ):
        self.G_file = G_file
        self.obs_file = obs_file
        self.sd_file = sd_file
        self.sites_filter_file = sites_filter_file
        
        self.B = basis_mat
        
        self.Ls = reg_mats
        self.reg_pars = reg_pars
        self.reg_par_names = reg_par_names
        assert len(self.Ls) = len(self.reg_pars)
        assert len(self.Ls) = len(self.reg_par_names)

        self.output_file = output_file        

    def _load_data(self):
        G_ep = EpochalG(self.G_file, self.sites_filter_file)
        self.G = G_ep(0)

        d_ep = EpochalDisplacement(self.obs_file, self.sites_filter_file)
        self.d = d_ep(0)

        sig_ep = EpochalDisplacementSD(self.sd_file, self.sites_filter_file)
        self.sig = sig_ep(0)
        

    def create_least_square_object(self):
        self._load_data()
        self.lease_squre = LeastSquareWithRegularization(
            G = self.G,
            d = self.d,
            sig = self.sig,
            Ls = self.Ls,
            B = self.B)

    def invert(self):
        
        self.create_least_square_object()

        ls = self.lease_squre
        
        ls.invert(*self.reg_pars)
        ls.predict()

        self.reg_mag = ls.get_reg_mag()
        self.nres_weighted = ls.get_residual_norm_weighted()
        self.nres = ls.get_residual_norm()
        

    


