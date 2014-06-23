from os.path import join

from pylab import savefig, close, clim

from viscojapan.plot_utils import Map
from viscojapan.inversion_test import GaussianSlip
from viscojapan.utils import get_this_script_dir

this_script_dir = get_this_script_dir(__file__)

def test():
    gaussian_slip = GaussianSlip()
    gaussian_slip.num_subflts_in_dip = 10
    gaussian_slip.num_subflts_in_strike = 25
    
    gaussian_slip.mu_dip = 4.
    gaussian_slip.mu_stk = 12.
    gaussian_slip.sig_dip = 2
    gaussian_slip.sig_stk = 5

    # temporal part
    gaussian_slip.max_slip0 = 10.
    gaussian_slip.log_mag = 1.
    gaussian_slip.tau = 5.

    t = 1100
    z = gaussian_slip(t)
    m = Map()
    m.init()
    m.plot_fslip(z)
    clim([0, gaussian_slip.max_slip(t)])
    savefig(join(this_script_dir,'gaussian_slip.pdf'))
    close()
