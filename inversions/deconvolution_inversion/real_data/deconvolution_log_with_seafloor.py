from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import Deconvolution
from viscojapan.inversion_test.l_curve import LCurve

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

project_path = '/home/zy/workspace/viscojapan/'


test = Deconvolution()

dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_d = 'cumu_post_with_seafloor.h5'
dtest.file_sig = 'sites_sd.h5'
dtest.sites_filter_file = 'sites_with_seafloor'
dtest.epochs = epochs_log

dtest.load_data()

lcurve = LCurve(dtest)
lcurve.outs_dir = 'outs_log'
lcurve.alphas = alphas
lcurve.betas = betas

lcurve.compute_L_curve()
