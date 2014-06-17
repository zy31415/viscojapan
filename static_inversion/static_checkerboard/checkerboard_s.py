import sys

from numpy import asarray

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import Map

from checkerboard_static import CheckerBoardStatic
from alphas import alphas

chb = CheckerBoardStatic()
chb.set_up()

sol = chb(alphas[3])
slip_inverted = asarray(sol['x']).reshape([10,25])

# plotting:
from pylab import *
m = Map()
m.init()
m.plot_fslip(slip_inverted)
show()

