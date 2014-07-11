from pylab import plt
from  numpy import dot

from viscojapan.least_square import LeastSquare, Roughening
from viscojapan.epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD
from viscojapan.plots import MapPlotFault
from viscojapan.plots import plot_L

from alphas import alphas

file_G = '/home/zy/workspace/viscojapan/greens_function/050km_static/G.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sig = 'sites_sd.h5'
sites_filter_file = 'sites_with_seafloor'

G_ep = EpochalG(file_G, sites_filter_file)
d_ep = EpochalDisplacement(file_d, sites_filter_file)
sig_ep = EpochalDisplacementSD(file_sig, sites_filter_file)

G = G_ep(0)
d = d_ep(0)
sig = sig_ep(0).flatten()


L = Roughening(
    ncols_slip = 35,
    nrows_slip = 10,
    col_norm_length = 1.,
    row_norm_length = 1.,    
    )()

nres_weighted = []
nroughs = []
for ano, alpha in enumerate(alphas):
    tik = LeastSquare(
        G = G,
        d = d,
        sig = sig,
        L = alpha * L)
    
    tik.invert()
    tik.predict()

    m1 = L.dot(tik.m)
    rough = dot(m1.T,m1)[0,0]
    

    nres_weighted.append(tik.get_residual_norm_weighted())
    nroughs.append(rough)

    mplt = MapPlotFault('fault_He50km.h5')   
    mplt.plot_slip(tik.m)
    
    mplt.plot_slip_contours(tik.m)
    plt.savefig('plots/co_%02d.png'%ano)
    #plt.show()
    plt.close()

plot_L(nres_weighted, nroughs, alphas)
plt.xlim([1, 20])
#plt.show()
plt.savefig('plots/L-curve.png')
plt.close()


