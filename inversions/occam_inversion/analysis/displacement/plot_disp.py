import sys

from pylab import *

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import Map, append_title
from viscojapan.slip import EpochalData
from days import days as epochs

disp_obs = EpochalData('cumu_post.h5')



ano=15
disp = EpochalData('../../outs_tik2/pred_disp_%02d.h5'%ano)
epochs = disp.get_epochs()

epoch = 1100
dd = disp.get_epoch_value(0)

sites = loadtxt('sites','4a')

m = Map()
m.region_code = 'near'
m.init()
m.plot_disp(dd,sites)

m.plot_disp(disp_obs.get_epoch_value(epoch),sites,color='red')

show()
