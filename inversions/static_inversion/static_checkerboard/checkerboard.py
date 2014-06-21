import pickle
from os.path import exists, join
from os import makedirs

from numpy import dot, asarray, amax, amin, logspace
from pylab import show,close, savefig, xlim

from viscojapan.least_square import LeastSquareTik2
from viscojapan.epochal_data import EpochalG
from viscojapan.inversion_test import gen_checkerboard_slip, gen_error_for_sites
from viscojapan.plot_epochal_data.plot_utils import Map
from viscojapan.plot_utils import plot_L
from viscojapan.utils import overrides

f_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
filter_site_file = 'sites'
filter_site_seafloor_file = 'sites_with_seafloor'


class CheckerboardTest(LeastSquareTik2):
    def __init__(self):
        super().__init__()
        self.f_G = f_G
        self.filter_site_file = None

    def _init_G(self):
        ep_G = EpochalG(self.f_G, self.filter_site_file)
        self.G = ep_G.get_epoch_value(0)
        self.sites = ep_G.filter_sites

    def _init_m_true(self):
        slip_true = gen_checkerboard_slip(10,25,2,3)
        self.m_true =  slip_true.flatten().reshape([-1,1])

    def _init_d_true(self):
        self._init_m_true()
        self.d_true = dot(self.G, self.m_true)

    def _init_d(self):
        self._init_d_true()
        self.num_sites = len(self.sites)

        self.east_st = self.north_st = 6e-3
        self.up_st = 20e-3

        error = gen_error_for_sites(self.num_sites,
                    self.east_st, self.north_st, self.up_st)
        self.d = self.d_true + error

    def _init_sig(self):
        self.sig = asarray([[self.east_st, self.north_st, self.up_st]*self.num_sites]).flatten()

    def init(self):
        self._init_G()
        self._init_d()
        self._init_sig()

    @overrides(LeastSquareTik2)
    def invert(self, alpha):
        super().invert(alpha, beta=0)

    def make_L_curve(self, alphas, outputs_dir):
        if not exists(outputs_dir):
            makedirs(outputs_dir)
        self.init()        
        nreses = []
        nroughs = []
        for ano, alpha in enumerate(alphas):
            self.invert(alpha)

            m = Map()
            m.init()            
            m.plot_fslip(self.m)
            #show()
            savefig(join(outputs_dir, 'slip_%02d.png'%ano))
            close()
            
            self.predict()    
            nres = self.get_residual_norm()
            nreses.append(nres)
            
            nrough = self.get_spatial_roughness()
            nroughs.append(nrough)

        plot_L(nreses, nroughs, alphas)

        x1 = amin(nreses)*0.9
        x2 = amax(nreses)*1.1
        
        xlim([x1,x2])
        savefig(join(outputs_dir, 'L-curve.png'))
        #show()
        close()

if __name__ =='__main__':
    alphas = logspace(-4,0,30)
    test1 = CheckerboardTest()
    test1.filter_site_file = filter_site_seafloor_file
    test1.make_L_curve(alphas, 'plots_with_seafloor')

    test2 = CheckerboardTest()
    test2.filter_site_file = filter_site_file
    test2.make_L_curve(alphas, 'plots')
