from numpy import logspace

from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix

epochs = [0]
fault_file = '../../greens_function/fault_He50km.h5'

basis = BasisMatrix.create_from_fault_file(fault_file)

rough = Roughening.create_from_fault_file(fault_file)

inv = OccamDeconvolution(
    file_G0 = '../../greens_function/G_Rake66.h5',
    files_Gs = ['../../greens_function/G_Rake90.h5'],
    nlin_par_names = ['rake'],
    file_d = '../../true_model/d_simu.h5',
    file_sd = '../../sites_sd/sites_sd.h5',
    file_incr_slip0 = 'slip0/slip0.h5',
    filter_sites_file = 'sites_with_seafloor',
    epochs = epochs,
    regularization = rough,
    basis = basis,          
    )
inv.set_data_except_L()

for nth, alpha in enumerate(logspace(-4, .1, 30)):
    reg = Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)
