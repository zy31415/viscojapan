import h5py
from pylab import *

from viscojapan.epochal_data import EpochalIncrSlip

ano = 16
bno = 19
incr_slip_ep = EpochalIncrSlip('../../outs_alpha_beta/incr_slip_a%02d_b%02d.h5'%(ano,bno))

incr_slip = incr_slip_ep.get_slip_at_subflt(5*25+13,0)

slip =[incr_slip[0]]
for ii in incr_slip[1:]:
    slip.append(slip[-1]+ii)

plot(slip)
show()
