import glob

from pylab import plt

import viscojapan as vj

def plot(fn, marker, label):
    result_file = fn
    fid = vj.inv.ResultFileReader(result_file)
    epochs = fid.epochs
    rms = fid.rms_inland_at_epoch

    plt.plot(epochs, rms, 'o-', label=label)    

# coupled model
result_file = '../../outs/nrough_06_naslip_11.h5'
plot(result_file, 'o-', 'SDco = 0.2')

result_file = '../../outs/nrough_06_naslip_10.h5'
plot(result_file, 'o-', 'SDco = 0.5')


plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (m)')

plt.legend(loc=0,prop={'size':10})
plt.savefig('mis_fit_comparison.png')
plt.show()


