from numpy import dot, asarray, hstack
from numpy.random import normal

from .static_inversion import StaticInversionTik2
from ..epochal_data import EpochalG
from ..fault.checkerboard import gen_checkerboard_slip

class CheckerboardTestForStaticInversion(StaticInversionTik2):
    def __init__(self):
        super().__init__()
        self.f_G = None
        self.filter_site_file = None

    def get_G(self):
        epochal_G = EpochalG(self.f_G, self.filter_site_file)
        G = epochal_G.get_epoch_value(0)
        return G

    def _get_fake_d(self):
        # generate observation 
        slip = gen_checkerboard_slip(25, 10, 2, 2)*5.

        m = slip.reshape((-1,1))

        d = dot(self.G,m)

        east_error = normal(0, 6e-3, (1300,1))
        north_error = normal(0, 6e-3, (1300,1))
        up_error = normal(0,20e-3,(1300,1))
        error = hstack((east_error, north_error, up_error))
        error_flat = error.flatten().reshape([-1,1])

        d += error_flat
        return d

    def get_d(self):
        return self._get_fake_d()
