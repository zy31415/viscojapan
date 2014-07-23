from numpy import logspace

import viscojapan as vj
from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix

from epochs_log import epochs
from alphas import alphas

fault_file = '../../fault_model/fault_He50km.h5'


basis = BasisMatrix.create_from_fault_file(fault_file, num_epochs = len(epochs))

rough_single = Roughening.create_from_fault_file(fault_file)
rough = vj.ExpandForAllEpochs(rough_single, len(epochs))
temp_reg = vj.TemporalRegularization.create_from_fault_file(fault_file, epochs)

inv = OccamDeconvolution(
    file_G0 = '../../greens_function/G_He50km_Vis5.8E18_Rake90.h5',
    
    files_Gs = ['../../green_function/G_He50km_Vis1.0E19_Rake90.h5',
                '../../green_function/G_He55km_Vis5.8E18_Rake90.h5',
                '../../green_function/G_He50km_Vis5.8E18_Rake95.h5'
                ],
    nlin_par_names = ['visM','He','rake'],

    file_d = '../cumu_post_with_seafloor.h5',
    file_sd = '../sites_sd/sites_sd.h5',
    file_incr_slip0 = 'slip0/incr_slip0.h5',
    filter_sites_file = 'sites_with_seafloor',
    epochs = epochs,
    regularization = rough,
    basis = basis,          
    )
inv.set_data_except_L()

for nth, alpha in enumerate(alphas):
    reg = Composite()
    reg.add_component(component = rough,
                      arg = alpha,
                      arg_name = 'roughening')
    reg.add_component(component = temp_reg,
                      arg = .07,
                      arg_name = 'temporal')
    
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)
