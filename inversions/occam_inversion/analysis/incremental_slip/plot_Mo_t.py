from pylab import *

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.slip import EpochalIncrSlip
from viscojapan.plot_utils import Map, append_title
from viscojapan.slip import EpochalIncrSlip
from days import days as epochs

def plot_Mw_t(ano,label=''):
    slip = EpochalIncrSlip('../../outs_tik2/incr_slip_%02d.h5'%ano)
    epochs = slip.get_epochs()

    mws = []
    for epoch in epochs:
        alpha = slip.get_info('alpha')
        s = slip.get_epoch_value(epoch)
        m = Map()
        m.region_code = 'near'
        #m.init()
        mo,mw = m.moment(s)
        mws.append(mw)
    print(mws)
    semilogx(epochs,mws,'o-',label=label)
    append_title(', ano = %d, alpha=%.3f'%(ano,alpha))

plot_Mw_t(13,'ano=13')
plot_Mw_t(14,'ano=14')
plot_Mw_t(15,'ano=15')
plot_Mw_t(16,'ano=16')
plot_Mw_t(17,'ano=17')
legend()
print(epochs)
show()

close()
