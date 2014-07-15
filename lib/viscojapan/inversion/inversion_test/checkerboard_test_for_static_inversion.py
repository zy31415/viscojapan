from os.path import exists, join
from os import makedirs

from numpy import dot, asarray, amax, amin, logspace, arange
from pylab import show,close, savefig, xlim
import scipy.sparse as sparse

from viscojapan.inversion_test import gen_checkerboard_slip, gen_error_for_sites
from viscojapan.plots import MapPlotFault, plot_L, MapPlotSlab
from viscojapan.utils import overrides
from viscojapan.least_square import LeastSquareWithRegularization, Roughening
from viscojapan.epochal_data import EpochalG
from viscojapan.basis_function import BasisMatrix
from viscojapan.fault_model import FaultFileIO

class CheckerboardTest():
    def __init__(self,
                 f_G,
                 filter_site_file,
                 fault_file,
                 dip_patch_size,
                 strike_patch_size,
                 sd_horizontal = 6e-3,
                 sd_up = 20e03,
                 ):

        self.f_G = f_G
        self.filter_site_file = filter_site_file
        self.fault_file = fault_file
        self.sd_horizontal = sd_horizontal
        self.sd_up = sd_up
        self.dip_patch_size = dip_patch_size
        self.strike_patch_size = strike_patch_size

        self._init_G()
        self._init_d()
        self._init_sig()
        self._init_L()
        self._init_B()
        
        self.tik = LeastSquareWithRegularization(
            G = self.G,
            d = self.d,
            sig = self.sig,
            Ls = [self.L2],
            B = self.B)
        
    @property
    def num_subflt_along_strike(self):
        f = FaultFileIO(self.fault_file)
        return f.num_subflt_along_strike

    @property
    def num_subflt_along_dip(self):
        f = FaultFileIO(self.fault_file)
        return f.num_subflt_along_dip
    
    def _init_L(self):
        L2 = Roughening(
            ncols_slip = self.num_subflt_along_strike,
            nrows_slip = self.num_subflt_along_dip,
            col_norm_length = 1.,
            row_norm_length = 1.,
            )()
        self.L2 = L2

    def _init_B(self):
        B = BasisMatrix(
            dx_spline = 20.,
            xf = arange(0,701, 20),
            dy_spline = 20.,
            yf = arange(0,221, 20),
            ).gen_basis_matrix_sparse()
        self.B = B
        
    def _init_G(self):
        ep_G = EpochalG(self.f_G, self.filter_site_file)
        self.sites = ep_G.filter_sites
        G = ep_G.get_epoch_value(0)
        self.G = G
    
    def _init_m_true(self):
        slip_true = gen_checkerboard_slip(
            self.num_subflt_along_dip,
            self.num_subflt_along_strike,
            dip_patch_size = self.dip_patch_size,
            strike_patch_size = self.strike_patch_size,)
        self.m_true =  slip_true.flatten().reshape([-1,1])

    def _init_d_true(self):
        self._init_m_true()
        self._init_B()
        self.d_true = dot(self.G, self.B.dot(self.m_true))

    def _init_d(self):
        self._init_d_true()
        self.num_sites = len(self.sites)

        self.east_st = self.north_st = self.sd_horizontal
        self.up_st = self.sd_up

        error = gen_error_for_sites(self.num_sites,
                    self.east_st, self.north_st, self.up_st)
        self.d = self.d_true + error


    def _init_sig(self):
        self.sig = asarray([[self.east_st, self.north_st, self.up_st]*self.num_sites]).\
                   reshape([-1, 1])
        

    def invert(self, alpha):
        self.tik.invert(alpha)

    def make_L_curve(self, alphas, outputs_dir):
        if not exists(outputs_dir):
            makedirs(outputs_dir)     
        nreses = []
        nroughs = []
        for ano, alpha in enumerate(alphas):
            self.invert([alpha])
            self.tik.predict() 

            mplt = MapPlotFault(self.fault_file)
            mplt.plot_slip(self.tik.Bm)
            mplt = MapPlotSlab()
            mplt.plot_top()
            #show()
            savefig(join(outputs_dir, 'slip_%02d.png'%ano))
            close()
            
               
            nres = self.tik.get_residual_norm_weighted()
            nreses.append(nres)
            
            nrough = self.tik.get_reg_mag()[0]
            nroughs.append(nrough)

        plot_L(nreses, nroughs, alphas)

        x1 = amin(nreses)*0.9
        x2 = amax(nreses)*1.1
        
        xlim([x1,x2])
        savefig(join(outputs_dir, 'L-curve.png'))
        #show()
        close()
