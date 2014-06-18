from numpy import asarray

from viscojapan.static_inversion import CheckerboardTestForStaticInversion
from viscojapan.plot_utils import Map

from checkerboard_static import CheckerBoardStatic
from alphas import alphas

chb = CheckerboardTestForStaticInversion()
chb.f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
chb.filter_site_file = 'sites'
alpha = 100

chb.load_data()
sol = chb.invert(alphas[3])

slip_inverted = asarray(sol['x']).reshape([10,25])

# plotting:
from pylab import *
m = Map()
m.init()
m.plot_fslip(slip_inverted)
show()

