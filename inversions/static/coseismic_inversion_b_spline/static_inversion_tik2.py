from pylab import plt
from  numpy import dot, arange, asarray
from multiprocessing import Queue, Pool
import pickle

from scipy.sparse import vstack

from viscojapan.least_square import LeastSquareWithRegularization, Roughening, Intensity
from viscojapan.epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD
from viscojapan.plots import MapPlotFault
from viscojapan.plots import plot_L
from viscojapan.basis_function import BasisMatrix

from alphas import alphas
from betas import betas

file_G = './greens_function/G.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sig = 'sites_sd.h5'
sites_filter_file = 'sites_with_seafloor'

G_ep = EpochalG(file_G, sites_filter_file)
d_ep = EpochalDisplacement(file_d, sites_filter_file)
sig_ep = EpochalDisplacementSD(file_sig, sites_filter_file)

G = G_ep(0)
d = d_ep(0)
sig = sig_ep(0)

L1 = Intensity(num_pars = 385)()

L2 = Roughening(
    ncols_slip = 35,
    nrows_slip = 11,
    col_norm_length = 1.,
    row_norm_length = 1.,    
    )()

B = BasisMatrix(
    dx_spline = 20.,
    xf = arange(0,701, 20),
    dy_spline = 20.,
    yf = arange(0,221, 20),
    ).gen_basis_matrix_sparse()


def invert(pars):
    bno = pars
    beta = betas[bno]
    tik = LeastSquareWithRegularization(
        G = G,
        d = d,
        sig = sig,
        Ls = [L2],
        B = B)
    tik.invert(alphas = [beta], nonnegative=True)
    tik.predict()

    nrough = tik.get_reg_mag()[0]
    
    nres = tik.get_residual_norm_weighted()

    invert.q.put((bno, nrough, nres))

    mplt = MapPlotFault('./fault_model/fault_He50km_east.h5')   
    mplt.plot_slip(tik.Bm)
    
    mplt.plot_slip_contours(tik.Bm)
    plt.savefig('plots/co_bno%02d.png'%(bno))
    #plt.show()
    plt.close()

def invert_init(q):
    invert.q = q

q = Queue()

nproc = 1
pool = Pool(nproc, invert_init, [q])

args = []
for bno, beta in enumerate(betas):
    args.append(bno)
pool.map(invert, args)

res = []
for arg in args:
    res.append(q.get())

with open('res.pkl','wb') as fid:
    pickle.dump(res, fid)

