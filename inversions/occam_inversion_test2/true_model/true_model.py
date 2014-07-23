from numpy import dot

from viscojapan.inversion.inversion_test import GaussianSlip, gen_error_for_sites
from viscojapan.plots import MapPlotFault, plt, MapPlotDisplacement
from viscojapan import EpochalG
import viscojapan as vj

if_plot = True

fault_file = '../greens_function/fault_He50km.h5'
gslip = GaussianSlip.create_from_fault_file(fault_file)

slip = gslip(0)

if if_plot:
    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(slip)
    plt.show()

file_G = '../greens_function/G_Rake80.h5'
g = EpochalG(file_G)
sites = g.sites

G = g(0)

d_pred = dot(G,slip.reshape([-1,1]))

if if_plot:
    mplt = MapPlotDisplacement()
    mplt.plot_disp(d_pred, sites)
    plt.show()

# add some error:
error = gen_error_for_sites(
    len(sites),
    east_st=6e-3, north_st=6e-3, up_st=20e-3)

d = d_pred + error

m_obj = vj.EpochalData('m_true.h5')
m_obj[0] = slip.reshape([-1,1])

d_obj = vj.EpochalData('d_simu.h5')
d_obj[0] = d
d_obj['sites'] = sites

