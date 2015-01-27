from pylab import *

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.plot_utils import Map, append_title
from viscojapan.inversion.slip import EpochalIncrSlip
from days import days as epochs

def plot_incr_slip(ano,epoch):
    slip = EpochalIncrSlip('../outs_tik2/incr_slip_%02d.h5'%ano)
    epochs = slip.get_epochs()

    alpha = slip.get_info('alpha')

    co_slip = slip.get_epoch_value(epoch)

    m = Map()
    m.region_code = 'near'
    m.init()
    s = slip.get_epoch_value(epochs[0])
    m.plot_fslip(co_slip)
    
    append_title(', ano = %d, alpha=%.3f, epoch=%d'%(ano,alpha,epoch))

##for ano in range(0,30):    
##    slip = EpochalSlip('../outs_tik2/slip_%02d.h5'%ano)
##    epochs = slip.get_epochs()
##
##    print(ano, slip.get_info('alpha'))
##
##    co_slip = slip.get_epoch_value(0)
##
##    m = Map()
##    m.region_code = 'near'
##    m.init()
##    s = slip.get_epoch_value(epochs[0])
##    m.plot_fslip(co_slip)
##
##    show()


ano = 15

for epoch in epochs:
    plot_incr_slip(ano, epoch)
    savefig('incr_slip_%04d.png'%epoch)
    close()
