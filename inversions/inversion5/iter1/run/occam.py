from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix

sys.path.append('../')
from epochs_log import epochs 
from alphas import alphas
from betas import betas

fault_file = '../fault_model/fault_bott40km.h5'


basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = '../green_function/G_He40km_Vis5.8E18_Rake81.h5',
    
    files_Gs = ['../green_function/G_He40km_Vis1.1E19_Rake81.h5',
                '../green_function/G_He45km_Vis5.8E18_Rake81.h5',
                '../green_function/G_He40km_Vis5.8E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','He','rake'],

    file_d = '../../cumu_post_with_seafloor.h5',
    file_sd = None,
    file_incr_slip0 = '../slip0/incr_slip0.h5',
    filter_sites_file = '../sites_with_seafloor',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )
inv.set_data_except(excepts=['L', 'sd','W'])

for bno, beta in enumerate(betas):
    if bno != 10:
        continue
    for ano, alpha in enumerate(alphas):
        if (ano < 9) or (ano > 13):
            continue
        for nsd in range(10):                
            outfname = 'outs/ano_%02d_bno_%02d_nsd_%02d.h5'%(ano, bno, nsd)
            if not exists(outfname):
                inv.regularization = \
                       reg = vj.create_roughening_temporal_regularization(
                           fault_file, epochs, alpha, beta)
                inv.set_data_L()

                inv.file_sd = '../../sd_seafloor/sd_files/sd_with_seafloor_%02d.h5'%nsd
                inv.set_data_sd()
                inv.set_data_W()
                
                inv.run()
                inv.save(outfname, overwrite=True)
            else:
                print("Skip %s !"%outfname)
                
