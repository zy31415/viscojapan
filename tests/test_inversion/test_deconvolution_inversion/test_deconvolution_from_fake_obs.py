from os.path import join

from numpy.random import normal

from viscojapan.deconvolution_inversion import DeconvolutionTestFromFakeObs
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

project_path = '/home/zy/workspace/viscojapan/'

def test():
    dtest = DeconvolutionTestFromFakeObs()

    dtest.file_G = join(project_path, 'greensfunction/050km-vis02/G.h5')
    dtest.file_fake_d = join(project_path, 'deconvolution_inversion/simulated_disp.h5')
    dtest.sites_filter_file = join(this_test_path, 'sites_0462')
    dtest.epochs = [0, 100, 1100]

    dtest.init()
    dtest.load_data()
    alpha = 1.
    dtest.invert(alpha)
