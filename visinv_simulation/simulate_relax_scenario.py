from viscojapan.gaussian_slip import GaussianSlip
from viscojapan.compute_displacement_in_viscous_media\
     import ComputeDisplacementInViscousMedia

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


com_disp = ComputeDisplacementInViscousMedia()
com_disp.file_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
com_disp.slip = gaussian_slip
com_disp.file_output = 'simulated_disp.h5'

com_disp.init()
com_disp.init_output_file()

# multiprocessing routine
com_disp.mp_add_epochs(range(1200),20)

# Single process
# com_disp.add_epochs(range(12))
