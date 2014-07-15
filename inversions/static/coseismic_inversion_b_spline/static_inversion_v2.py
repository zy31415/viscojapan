from numpy import arange, logspace

from viscojapan.inversion.basis_function import BasisMatrix
from viscojapan.inversion.regularization import Roughening
from viscojapan.inversion.static.static_inversion import StaticInversion
from viscojapan.inversion.static.compute_L_curve import ComputeLCurve

fault_file = './fault_model/fault_He50km_east.h5'

L2_obj = Roughening.create_from_fault_file(fault_file)
L2 = L2_obj()

B_obj = BasisMatrix.create_from_fault_file(fault_file)
B = B_obj.gen_basis_matrix_sparse()

inv = StaticInversion(
    G_file = './greens_function/G.h5',
    obs_file = 'cumu_post_with_seafloor.h5',
    sd_file = 'sites_sd.h5',
    sites_filter_file = 'sites_with_seafloor',
    Ls = [L2],
    B = B,
    output_dir = 'outs/'
)

alphas = logspace(-3, 1, 30)

lcurve = ComputeLCurve(
    inversion = inv,
    args = [alphas],
    outputs_dir = 'outs/'
    )

if __name__ == '__main__':
    lcurve.run_mp(4)
