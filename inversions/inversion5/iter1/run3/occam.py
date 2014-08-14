from numpy import logspace
from os.path import exists
import sys

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import \
     create_temporal_edge_roughening
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs
from reg_edges import reg_edges
from reg_roughes import reg_roughes


fault_file = '../fault_model/fault_bott40km.h5'

# nseasd  sd
# 0     0.0001
# 1     0.00564444444444
# 2     0.0111888888889
nseasd = 1


basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = OccamDeconvolution(
    file_G0 = '../green_function/G_He40km_Vis5.8E18_Rake81.h5',
    
    files_Gs = ['../green_function/G_He40km_Vis1.1E19_Rake81.h5',
                '../green_function/G_He45km_Vis5.8E18_Rake81.h5',
                '../green_function/G_He40km_Vis5.8E18_Rake90.h5'
                ],
    nlin_par_names = ['log10(visM)','He','rake'],

    file_d = '../../cumu_post_with_seafloor.h5',
    file_sd = '../../sd_seafloor/sd_files/sd_with_seafloor_%02d.h5'%nseasd,
    file_incr_slip0 = '../slip0/incr_slip0.h5',
    filter_sites_file = '../sites_with_seafloor',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )

inv.set_data_except(excepts=['L',])

reg_temp = 0.1
for reg_rough, nrough in enumerate(reg_roughes):
    for reg_edge, nedge in enumerate(reg_edges):
        outfname = 'outs/seasd_%02d_nrough_%02d_nedge_%02d.h5'%(nseasd, nrough, nedge)
        if not exists(outfname):
            inv.regularization = \
                   reg = vj.create_temporal_edge_roughening(
                       fault_file, epochs, reg_temp, reg_edge, reg_rough)
            inv.set_data_L()            
            inv.run()
            inv.save(outfname, overwrite=True)
        else:
            print("Skip %s !"%outfname)
                
