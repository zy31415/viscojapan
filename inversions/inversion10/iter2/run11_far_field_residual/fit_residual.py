import numpy as np

import viscojapan as vj
from viscojapan.inversion.occam_deconvolution.formulate_occam import JacobianVec

from epochs import epochs

file_G0 = '../green_function/G0_He50km_VisM6.3E18_Rake83.h5'
file_G1 = '../green_function/G1_He50km_VisM1.0E19_Rake83.h5'

#epochs = [0, 10, 20]

sites = vj.utils.as_string(np.loadtxt('sites_far', '4a', usecols=(0,)))

G0 = vj.inv.ep.EpochG(file_G0, mask_sites = sites)
G1 = vj.inv.ep.EpochG(file_G1, mask_sites = sites)

diffG = vj.inv.ep.DifferentialG(G0, G1, wrt='log10(visM)')

slip = vj.inv.ep.EpochSlip('slip.h5')

jecVec = JacobianVec(diffG, slip)

jec_vec = jecVec(epochs)


obs_disp = vj.inv.ep.EpochDisplacement('obs_disp.h5', mask_sites = sites)
pred_disp = vj.inv.ep.EpochDisplacement('pred_disp.h5', mask_sites = sites)

obs_disp_vec = obs_disp.stack(epochs)
pred_disp_vec = pred_disp.stack(epochs)

diff_disp_vec = obs_disp_vec - pred_disp_vec

del_eta = np.dot(-diff_disp_vec.T, jec_vec)/(np.linalg.norm(jec_vec)**2)

print(del_eta)
