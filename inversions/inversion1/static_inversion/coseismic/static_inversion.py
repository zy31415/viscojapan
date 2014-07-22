from numpy import logspace

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.static_inversion import StaticInversion


fault_file = '../../fault_model/fault_He50km_east.h5'

rough = Roughening.create_from_fault_file(fault_file)

basis = BasisMatrix.create_from_fault_file(fault_file)

inv = StaticInversion(
    file_G = '../../greens_function/G.h5',
    file_d = 'cumu_post_with_seafloor.h5',
    file_sd = 'sites_sd.h5',
    file_sites_filter = 'sites_with_seafloor',
    regularization = None,
    basis = basis,
)
inv.set_data_except_L()

for nth, alpha in enumerate(logspace(-3, 1, 30)):
    reg = Composite().add_component(component = rough,
                                    arg = alpha,
                                    arg_name = 'roughening')
    inv.regularization = reg
    inv.set_data_L()
    inv.invert()
    inv.predict()
    inv.save('outs/ano_%02d.h5'%nth, overwrite=True)
