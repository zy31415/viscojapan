from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.inversion import Deconvolution
from viscojapan.inversion.regularization import \
     TemporalRegularization, Roughening, Composite, \
     create_roughening_temporal_regularization
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

file_G = '../../../greens_function/G.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sd = 'sites_sd.h5'
file_sites_filter = 'sites_with_seafloor'

fault_file = '../../../fault_model/fault_He50km_east.h5'

#epochs_log = [0, 10, 20]

basis = BasisMatrix.create_from_fault_file(
    fault_file, len(epochs_log))
   
inv = Deconvolution(
    file_G = file_G,
    file_d = file_d,
    file_sd = file_sd,
    file_sites_filter = file_sites_filter,
    epochs = epochs_log,
    regularization = None,
    basis = basis
    )
inv.set_data_except_L()

bno = 10
beta = betas[bno]
for ano, alpha in enumerate(alphas):
    inv.regularization = \
           reg = create_roughening_temporal_regularization(
               fault_file, epochs_log, alpha, beta)
    inv.set_data_L()
    inv.run()
    inv.save('outs/ano_%02d_bno_%02d.h5'%(ano, bno), overwrite=True)
        
