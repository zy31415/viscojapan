from pylab import *

from viscojapan.plot_utils import Map, append_title
from viscojapan.epochal_data import EpochalIncrSlip
from epochs_log import epochs

def plot_Mw_t(ano,label=''):
    slip = EpochalIncrSlip('../../outs_log/incr_slip_a%02d_b10.h5'%ano)
    epochs = slip.get_epochs()

    mws = []
    mos = []
    for epoch in epochs[1:]:
        alpha = slip.get_info('alpha')
        s = slip.get_epoch_value(epoch)
        m = Map()
        m.region_code = 'near'
        #m.init()
        mo,mw = m.moment(s)
        mws.append(mw)
        mos.append(mo)
        
    plot(epochs[1:],mos,'o-',label=label)
    append_title(', ano = %d, alpha=%.3f'%(ano,alpha))

plot_Mw_t(10,'ano=10')
##plot_Mw_t(14,'ano=14')
##plot_Mw_t(15,'ano=15')
##plot_Mw_t(16,'ano=16')
##plot_Mw_t(17,'ano=17')
legend()
print(epochs)
xlim([-100, 1200])

show()
close()
