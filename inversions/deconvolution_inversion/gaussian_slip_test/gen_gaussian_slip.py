from pylab import *

from viscojapan.plot_utils import Map
from viscojapan.epochal_data import EpochalData
from viscojapan.gaussian_slip import GaussianSlip

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


obj = EpochalData('gaussian_slip.h5')
for epoch in range(0,1200):
    obj.set_epoch_value(epoch, gaussian_slip(epoch))

