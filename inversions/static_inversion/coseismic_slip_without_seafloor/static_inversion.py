from viscojapan.least_square import LeastSquareTik2
from viscojapan.epochal_data import \
     EpochalG, EpochalDisplacement,EpochalDisplacementSD
from viscojapan.plots.plot_utils import Map, plt
from viscojapan.plots.plot_res_file import plot_L

from alphas import alphas

file_G = '/home/zy/workspace/viscojapan/greensfunction/050km-vis02/G.h5'
file_d = 'cumu_post_with_seafloor.h5'
file_sig = 'sites_sd.h5'
sites_filter_file = 'sites'

G = EpochalG(file_G, sites_filter_file)
d = EpochalDisplacement(file_d, sites_filter_file)
sig = EpochalDisplacementSD(file_sig, sites_filter_file)

tik = LeastSquareTik2()
tik.G = G(0)
tik.d = d(0)
tik.sig = sig(0).flatten()

nres_weighted = []
nroughs = []
for ano, alpha in enumerate(alphas):
    tik.invert(alpha,0.)
    
    tik.predict()

    nres_weighted.append(tik.get_residual_norm_weighted())
    nroughs.append(tik.get_spatial_roughness())

    m = Map()   
    m.plot_fslip(tik.m)
    m.plot_slip_contours(tik.m)
    plt.savefig('plots/co_%02d.png'%ano)
    #plt.show()
    plt.close()

plot_L(nres_weighted, nroughs, alphas)
plt.show()
plt.savefig('L-curve.png')
plt.close()


