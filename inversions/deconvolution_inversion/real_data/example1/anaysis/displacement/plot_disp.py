from pylab import *

from viscojapan.plot_utils import Map, append_title
from viscojapan.epochal_data import EpochalDisplacement
from epochs_log import epochs


file_sites = 'sites_with_seafloor'
epoch = 1100

disp_obs = EpochalDisplacement('cumu_post_with_seafloor.h5',file_sites)
aslip_obs = disp_obs.get_epoch_value(epoch) - disp_obs.get_epoch_value(0)

sites = disp_obs.get_info('sites')
ano = 10
bno = 15
disp_pred = EpochalDisplacement('../../outs_log/pred_disp_a%02d_b%02d.h5'%(ano,bno),
                           file_sites)

#disp_pred = EpochalDisplacement('../../res_pred_disp.h5', file_sites)

aslip_pred = disp_pred.get_epoch_value(epoch) - disp_pred.get_epoch_value(0)

m = Map()
m.region_code = 'near'
scale = 10

m.region_code = 'I'
scale = 0.5

m.region_code = 'H'
scale = 1.2

m.init()


m.plot_disp(aslip_obs,sites, scale=scale)
m.plot_disp(aslip_pred,sites,color='red', scale=scale)

show()
