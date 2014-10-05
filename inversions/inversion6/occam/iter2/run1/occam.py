from numpy import logspace
from os.path import exists

import viscojapan as vj
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix

from epochs import epochs
from reg_roughes import reg_roughes

fault_file = '../fault_model/fault_bott50km.h5'

basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

inv = vj.OccamDeconvolutionSeparateCoPost2(
    file_G0 = '../green_function/G_He50km_Vis2.8E19_Rake90.h5',
    
    files_Gs = ['../green_function/G_He50km_Vis4.0E19_Rake90.h5',
                '../green_function/G_He45km_Vis2.8E19_Rake90.h5',
                '../green_function/G_He50km_Vis2.8E19_Rake85.h5'
                ],
    nlin_par_names = ['log10(visM)','log10(He)','rake'],

    file_d = '../obs/post_obs.h5',
    file_sd = 'sd/sd_hor_1_ver_5_sea_inf.h5',
    file_incr_slip0 = 'slip0/incr_slip0.h5',
    file_co_slip = 'slip0/incr_slip0.h5',
    filter_sites_file = 'sites_without_seafloor',
    epochs = epochs,
    regularization = None,
    basis = basis,          
    )
inv.set_data_except_L()

reg_temp = 0
reg_edge = 0.06
for nrough, reg_rough in enumerate(reg_roughes):
    outfname = 'outs/nrough_%02d.h5'%(nrough)
    if exists(outfname):
        print("Skip %s !"%outfname)
        continue
    print(outfname)
    inv.regularization = \
           reg = vj.create_temporal_edge_roughening(
               fault_file, epochs, reg_temp, reg_edge, reg_rough)
    
    inv.set_data_L()
    inv.run()
    inv.save(outfname, overwrite=True)
