from pylab import *

from viscojapan.plot_utils import Map
from viscojapan.gaussian_slip import GaussianSlip

gaussian_slip = GaussianSlip()
t = 1100
z = gaussian_slip(t)
m = Map()
m.init()
m.plot_fslip(z)
clim([0, gaussian_slip.max_slip(t)])
show()
