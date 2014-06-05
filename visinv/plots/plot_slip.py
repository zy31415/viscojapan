import sys

from pylab import *

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import Map
from viscojapan.slip import EpochalSlip

for ano in range(0,30):    
    slip = EpochalSlip('../outs_tik2/slip_%02d.h5'%ano)
    epochs = slip.get_epochs()

    print(ano, slip.get_info('alpha'))

    co_slip = slip.get_epoch_value(0)

    m = Map()
    m.region_code = 'near'
    m.init()
    s = slip.get_epoch_value(epochs[0])
    m.plot_fslip(co_slip)

    show()
