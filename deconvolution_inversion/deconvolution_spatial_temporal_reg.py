from os.path import join

from numpy import logspace
from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir, delete_if_exists

from epochs_even import epochs as epochs_even


project_path = '/home/zy/workspace/viscojapan/'

dtest = DeconvolutionTestFromFakeObs()
dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
dtest.file_d = 'simulated_disp.h5'
dtest.sites_filter_file = 'sites'
dtest.epochs = epochs_even
dtest.num_err = 1300*len(epochs_even)

dtest.load_data()

alphas = logspace(-4,3,30)
betas = logspace(-4,3,30)

for ano, alpha in enumerate(alphas):
    for bno, beta in enumerate(betas):
        dtest.invert(alpha, beta)
        dtest.predict()
        dtest.res_writer.save_results('outs_alpha_beta/res_a%02d_b%02d.h5'%(ano,bno))
        dtest.res_writer.save_results_incr_slip('outs_alpha_beta/incr_slip_a%02d_b%02d.h5'%(ano,bno))
        dtest.res_writer.save_results_slip('outs_alpha_beta/slip_a%02d_b%02d.h5'%(ano,bno))
        dtest.res_writer.save_results_pred_disp('outs_alpha_beta/pred_disp_a%02d_b%02d.h5'%(ano,bno))

