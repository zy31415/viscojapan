from pylab import plt

import viscojapan as vj

def plot_slip(slip, nx, ny,
              label='x-',
              legend = None
              ):
    epochs = slip.get_epochs()
    s = slip.get_cumu_slip_at_subfault(nx, ny)
    plt.plot(epochs, s, label, label=legend)


res_file = '../../outs/nrough_05_naslip_11.h5'
reader = vj.inv.ResultFileReader(res_file)
slip_pred = reader.get_slip()

slip_exp = vj.epoch_3d_array.Slip.load('extra_slip_EXP.h5')
slip_log = vj.epoch_3d_array.Slip.load('extra_slip_LOG.h5')


nx = 1
ny = 1

plot_slip(slip_pred, nx, ny, label='x-', legend='Pred.')
plot_slip(slip_exp, nx, ny, label='^-', legend='EXP')
plot_slip(slip_log, nx, ny, label='o-', legend='LOG')

plt.legend(loc=0)
plt.savefig('extra_%d_%d.png'%(nx, ny))
plt.show()    
