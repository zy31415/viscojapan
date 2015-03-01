import glob

from pylab import plt

import viscojapan as vj

def plot(fn, marker, label):
    result_file = fn
    fid = vj.inv.ResultFileReader(result_file)
    epochs = fid.epochs
    rms = fid.rms_inland_at_epoch

    plt.plot(epochs, rms, 'o-', label=label)    

# no Raslip model
result_file = '../../../run2/outs/nrough_06_naslip_11.h5'
plot(result_file, 'o-', 'no-Ralsip SDco = .2')

# coupled model
result_file = '../../../../../../inversion10/iter2/run11/outs/nrough_06_naslip_11.h5'
plot(result_file, 'o-', 'Coupled SDco = 0.2')
##
##result_file = '../../../run1/outs/nrough_06_naslip_11.h5'
##plot(result_file, 'o-', 'SDco = 1')
##
##result_file = '../../../run2/outs/nrough_06_naslip_11.h5'
##plot(result_file, 'o-', 'SDco = .2')

plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (m)')

plt.legend(loc=0,prop={'size':10})
plt.savefig('mis_fit_comparison.png')
plt.show()


