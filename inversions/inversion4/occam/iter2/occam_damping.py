from numpy import logspace

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import Roughening, Composite, Intensity
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs 
from alphas import alphas
from gammas import gammas

fault_file = 'fault_model/fault_bott33km.h5'


basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = 'green_function/G_He33km_Vis5.8E18_Rake83.h5',
    
    files_Gs = ['green_function/G_He33km_Vis1.1E19_Rake83.h5',
                'green_function/G_He45km_Vis5.8E18_Rake83.h5',
                'green_function/G_He33km_Vis5.8E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','He','rake'],

    file_d = '../cumu_post_with_seafloor.h5',
    file_sd = '../sites_sd/sites_sd.h5',
    file_incr_slip0 = 'slip0/incr_slip0.h5',
    filter_sites_file = 'sites_with_seafloor',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )
inv.set_data_except_L()

alpha = 0.015
beta = 0.2

for cno, gamma in enumerate(gammas):
    outfname = 'outs/cno_%02d.h5'%(cno)
    if not exists(outfname):
        inv.regularization = \
               reg = vj.create_roughening_temporal_intensity_regularization(
                   fault_file, epochs, alpha, beta, gamma)
        inv.set_data_L()
        inv.run()
        inv.save(outfname, overwrite=True)
    else:
        print("Skip %s !"%outfname)
            
