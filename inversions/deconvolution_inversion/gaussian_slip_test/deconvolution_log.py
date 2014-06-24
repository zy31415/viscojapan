from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

project_path = '/home/zy/workspace/viscojapan/'

outs_dir = 'outs_alpha_beta_log'

dtest = DeconvolutionTestFromFakeObs()
dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_d = 'simulated_disp.h5'
dtest.sites_filter_file = 'sites'
dtest.epochs = epochs_log

dtest.num_err = 1300*len(epochs_log)
dtest.east_st=6e-3
dtest.north_st=6e-3
dtest.up_st=20e-3

dtest.load_data()

dtest.alphas = alphas
dtest.betas = betas
dtest.outs_dir = outs_dir

dtest.compute_L_curve()
