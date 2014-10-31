from numpy import logspace

from viscojapan.inversion import OccamDeconvolution
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.basis_function import BasisMatrix, BasisMatrixBSpline

epochs = [0]
fault_file = '../../fault_model/fault_bott60km.h5'

basis = BasisMatrix.create_from_fault_file(fault_file)
basis_b_spline = BasisMatrixBSpline.create_from_fault_file(fault_file)

rough = Roughening.create_from_fault_file(fault_file)

inv = OccamDeconvolution(
    file_G0 = '../../green_function/G0_He63km_VisM1.0E19_Rake90.h5',
    files_Gs = ['../../green_function/G1_He63km_VisM1.0E19_Rake80.h5'],
    nlin_par_names = ['rake'],
    file_d = '../../cumu_post_with_seafloor.h5',
    file_sd = '../sd/sd_seafloor_inf.h5',
    file_incr_slip0 = 'slip0/slip0.h5',
    filter_sites_file = 'sites_with_seafloor',
    epochs = epochs,
    regularization = rough,
    basis = basis_b_spline,          
    )
inv.set_data_except_L()

for nth, alpha in enumerate(logspace(-4, 0, 30)):
    reg = Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)
