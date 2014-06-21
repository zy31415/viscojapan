from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists

from epochs_log import epochs as epochs_log

from alphas import alphas

project_path = '/home/zy/workspace/viscojapan/'

dtest = DeconvolutionTestFromFakeObs()
dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_fake_d = 'simulated_disp.h5'
dtest.sites_filter_file = 'sites'
dtest.epochs = epochs_log

dtest.init()
dtest.load_data()

for ano, alpha in enumerate(alphas):
    dtest.invert(alpha)
    dtest.res_writer.save_results('outs_log_spacing/res_%02d.h5'%ano)
    dtest.res_writer.save_results_incr_slip('outs_log_spacing/incr_slip_%02d.h5'%ano)
    dtest.res_writer.save_results_slip('outs_log_spacing/slip_%02d.h5'%ano)    
    dtest.res_writer.save_results_pred_disp('outs_log_spacing/pred_disp_%02d.h5'%ano)

