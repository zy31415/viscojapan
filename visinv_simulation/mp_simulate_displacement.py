from multiprocessing import Pool
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

simu_disp_file = 'simulated_disp.h5'
simu_disp = EpochalData(simu_disp_file)

for key in 'sites', 'He', 'lmax', 'visK', 'visM', 'log10_visM':
    val = G.get_info(key)
    simu_disp.set_info(key, val)

def compute_epoch(epoch):
    print('Day = %d'%epoch)
    try:    
        T = gaussian_slip(0).reshape([-1,1])
        D = dot(G(epoch),T)
        for jj in range(1, epoch):
            T = gaussian_slip(jj) - gaussian_slip(jj-1)
            T = T.reshape([-1,1])
            D += dot(G(epoch-jj),T)
        simu_disp.set_epoch_value(epoch, D)
    except:
        

if __name__ == '__main__':
    with Pool(processes=20) as pool:
        pool.map(compute_epoch, range(1200))

