from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import Deconvolution
from viscojapan.inversion_test.l_curve import LCurve

from epochs_log import epochs as epochs_log
from alphas import alphas
from betas import betas

project_path = '/home/zy/workspace/viscojapan/'


dtest = Deconvolution()

dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_d = 'cumu_post_with_seafloor.h5'
dtest.file_sig = 'sites_sd.h5'
dtest.sites_filter_file = 'sites_with_seafloor'
dtest.epochs = epochs_log

dtest.load_data()

dtest.invert(alpha = 30., beta = 16.)
dtest.predict()

dtest.res_writer.save_results('res.h5')
dtest.res_writer.save_results_incr_slip('res_incr_slip.h5')
dtest.res_writer.save_results_slip('res_slip.h5')
dtest.res_writer.save_results_pred_disp('res_pred_disp.h5')
