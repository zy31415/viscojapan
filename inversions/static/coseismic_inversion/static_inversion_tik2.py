from pylab import plt
from  numpy import dot
from multiprocessing import Queue, Pool
import pickle

from scipy.sparse import vstack

from viscojapan.least_square import LeastSquare, Roughening, Intensity
from viscojapan.epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD
from viscojapan.plots import MapPlotFault
from viscojapan.plots import plot_L

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

def invert(pars):
    bno = pars
    beta = betas[bno]
    L = beta * L2
    tik = LeastSquare(
        G = G,
        d = d,
        sig = sig,
        L = L)
    tik.invert(nonnegative=True)
    tik.predict()

    tp = L2.dot(tik.m)
    nrough = dot(tp.T,tp)[0,0]

    nres = tik.get_residual_norm_weighted()

    invert.q.put((bno, nrough, nres))

    mplt = MapPlotFault('./fault_model/fault_He50km_east.h5')   
    mplt.plot_slip(tik.m)
    
    mplt.plot_slip_contours(tik.m)
    plt.savefig('plots/co_bno%02d.png'%(bno))
    #plt.show()
    plt.close()

def invert_init(q):
    invert.q = q

q = Queue()

nproc = 4
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

##
##plot_L(nres_weighted, nroughs, alphas)
##plt.xlim([1, 20])
###plt.show()
##plt.savefig('plots/L-curve.png')
##plt.close()
##
##
