from numpy import dot

from viscojapan.inversion.inversion_test import GaussianSlip, gen_error_for_sites
from viscojapan.plots import MapPlotFault, plt, MapPlotDisplacement
import viscojapan as vj

if_plot = True

fault_file = '../../fault_model/fault_bott80km.h5'

dip_patch_size = 3
strike_patch_size = 4

#gslip = GaussianSlip.create_from_fault_file(fault_file)
slip = vj.inv.test.gen_checkerboard_slip_from_fault_file(
    fault_file,
    dip_patch_size = dip_patch_size,
    strike_patch_size = strike_patch_size)

slip *= 2.
if if_plot:
    mplt = MapPlotFault(fault_file)
    mplt.plot_slip(slip,
                   zorder=-2,
                   cb_shrink=0.7,
                   cb_pad = 0.1)
    mplt = vj.plots.MapPlotSlab()
    mplt.plot_top()
    
    #plt.show()
    plt.savefig('slip_d_simu_dip%d_stk%d.png'%(dip_patch_size, strike_patch_size))
    plt.savefig('slip_d_simu_dip%d_stk%d.pdf'%(dip_patch_size, strike_patch_size))
    plt.close()

file_G = '../../green_function/G0_He50km_VisM6.3E18_Rake83.h5'
g = vj.inv.ep.EpochG(file_G)
sites = g.get_sites()

G = g.get_data_at_epoch(0)

d_pred = dot(G,slip.reshape([-1,1]))

if if_plot:
    mplt = MapPlotDisplacement()
    mplt.plot_disp(d_pred, sites)
    #plt.show()
    plt.savefig('disp_d_simu_dip%d_stk%d.png'%(dip_patch_size, strike_patch_size))
    plt.close()

# add some error:
error = gen_error_for_sites(
    len(sites),
    east_st=3e-3, north_st=3e-3, up_st=10e-3)

d = d_pred + error
d = d.reshape([1,-1,3])

d3d = vj.epoch_3d_array.EpochSites3DArray(d, [0], sites)

d3d.save('d_simu_dip%d_stk%d.h5'%(dip_patch_size, strike_patch_size))
