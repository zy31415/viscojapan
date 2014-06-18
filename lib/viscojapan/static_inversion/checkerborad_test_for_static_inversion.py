from numpy import dot, asarray, hstack
from numpy.random import normal

from .static_inversion import StaticInversionTik2
from ..epochal_data import EpochalG
from ..fault.checkerboard import gen_checkerboard_slip
from ..utils import gen_error_for_sites, overrides

class CheckerboardTestForStaticInversion(StaticInversionTik2):
    def __init__(self):
        super().__init__()
        self.f_G = None
        self.filter_site_file = None

    @overrides(StaticInversionTik2)
    def _load_G(self):
        epochal_G = EpochalG(self.f_G, self.filter_site_file)
        G = epochal_G.get_epoch_value(0)
        return G

    def _gen_fake_d(self):
        # generate observation 
        slip = gen_checkerboard_slip(25, 10, 2, 2)*5.

        m = slip.reshape((-1,1))

        d = dot(self.G,m)

        error = gen_error_for_sites(1300)
        d += error
        return d

    @overrides(StaticInversionTik2)
    def _load_d(self):
        return self._gen_fake_d()
