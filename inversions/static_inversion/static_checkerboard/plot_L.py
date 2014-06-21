import pickle
import sys

from pylab import *

from alphas import alphas

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import plot_L

with open('L-curve.pkl','rb') as fid:
    nres, nrough = pickle.load(fid)

plot_L(nres, nrough, alphas)
show()
