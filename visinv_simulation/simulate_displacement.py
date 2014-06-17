from numpy import dot

from viscojapan.epochal_data.epochal_data import EpochalData
from viscojapan.gaussian_slip import GaussianSlip

# simulated slip on the fault
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

# G matrix
G = EpochalData('/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5')

for ii in range(1200):
    print(ii)
    T = gaussian_slip(0).reshape([-1,1])
    D = dot(G(ii),T)
    for jj in range(1,ii):
        T = gaussian_slip(jj) - gaussian_slip(jj-1)
        T = T.reshape([-1,1])
        D += dot(G(ii-jj),T)
