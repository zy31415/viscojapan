import h5py
from pylab import *

from viscojapan.epochal_data import EpochalIncrSlip

ano = 29

incr_slip_ep = EpochalIncrSlip('../../outs0/slip_%02d.h5'%ano)

from days import days as epochs    

incr_slips = []
m = 9
n = 12
for epoch in epochs:
    incr_slip = incr_slip_ep(epoch).reshape([10,25])
    incr_slips.append(incr_slip[m,n])

ys = [incr_slips[0]]
for ii in incr_slips[1:]:
    ys.append(ii + ys[-1])


from viscojapan.gaussian_slip import GaussianSlip
from viscojapan.deconvolution_inversion import ForwardConvolution

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

ys_predicted = []
for epoch in epochs:
    tp = gaussian_slip(epoch)
    ys_predicted.append(tp[m,n])

plot(epochs, ys, marker='o', label='inverted')
plot(epochs, ys_predicted, marker='o', label='true')
legend()
xlim([-100, 1200])
#ylim([7, 14])
grid('on')
show()
    
