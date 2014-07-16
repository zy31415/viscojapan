from numpy import arange, logspace

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening, Composite
from viscojapan.inversion.static_inversion import StaticInversion
#from viscojapan.inversion.static.compute_L_curve import ComputeLCurve

fault_file = './fault_model/fault_He50km_east.h5'

rough = Roughening.create_from_fault_file(fault_file)
reg = Composite().add_component(rough, 1., 'roughening')

basis = BasisMatrix.create_from_fault_file(fault_file)

inv = StaticInversion(
    file_G = './greens_function/G.h5',
    file_d = 'cumu_post_with_seafloor.h5',
    file_sd = 'sites_sd.h5',
    file_sites_filter = 'sites_with_seafloor',
    regularization = reg,
    basis = basis,
)

inv.run()
inv.write_outputs('~out.h5', overwrite=True)
