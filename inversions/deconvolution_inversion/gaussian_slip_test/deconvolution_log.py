from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists
from viscojapan.inversion_test.l_curve import LCurve

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

project_path = '/home/zy/workspace/viscojapan/'

outs_dir = 'outs_log'

dtest = DeconvolutionTestFromFakeObs()
dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_d = 'simulated_disp.h5'
dtest.sites_filter_file = 'sites_with_seafloor'
dtest.epochs = epochs_log

dtest.num_err = 1300*len(epochs_log)
dtest.east_st=6e-3
dtest.north_st=6e-3
dtest.up_st=20e-3

dtest.load_data()

lcurve = LCurve(dtest)
lcurve.outs_dir = 'outs_log'
lcurve.alphas = alphas
lcurve.betas = betas

lcurve.compute_L_curve()
