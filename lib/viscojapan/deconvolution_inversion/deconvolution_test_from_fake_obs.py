from numpy.random import normal

from viscojapan.deconvolution_inversion import Deconvolution
from viscojapan.utils import gen_error_for_sites, overrides

class DeconvolutionTestFromFakeObs(Deconvolution):
    def __init__(self):
        super().__init__()
        self.file_G = None
        self.file_fake_d = None
        self.sites_filter_file = None
        self.epochs = []

    def init(self):
        super().init()
        self.file_d = self.file_fake_d

    @overrides(Deconvolution)
    def _load_d(self):
        d = super()._load_d()
        num_obs = len(d)
        assert num_obs%3 == 0, 'Wrong number of observations.'
        num_sites = num_obs//3
        error = gen_error_for_sites(num_sites)
        d += error
        return d
