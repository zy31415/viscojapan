from os.path import join, exists

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

file_G = '../green_function/G_He33km_Vis5.8E18_Rake83.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sd = 'sites_sd.h5'
file_sites_filter = 'sites_with_seafloor'

fault_file = '../fault_model/fault_bott33km.h5'


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


betas = [betas[10]]

for bno, beta in enumerate(betas):
    for ano, alpha in enumerate(alphas):
        outfname = 'outs/ano_%02d_bno_%02d.h5'%(ano, bno)
        if not exists(outfname):
            inv.regularization = \
                   reg = create_roughening_temporal_regularization(
                       fault_file, epochs_log, alpha, beta)
            inv.set_data_L()
            inv.run()
            inv.save(outfname, overwrite=True)
        else:
            print("Skip %s !"%outfname)
            
