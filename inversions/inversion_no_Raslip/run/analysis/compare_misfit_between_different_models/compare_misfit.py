import glob

from pylab import plt

import viscojapan as vj

## static model
files = sorted(glob.glob('../../../static_inversion/outs/outs_????/rough_16.h5'))

rmses = []
epochs = []
for file in files:
    epochs.append((int(file.split('/')[-2][-4:])))
    with vj.inv.ResultFileReader(
        file) as reader:
        rms = reader.rms_inland
        rmses.append(rms)
plt.plot(epochs, rmses, '^-', label='slip only model')

# no Raslip model
result_file_no_Raslip = '../../outs/nrough_06_naslip_11.h5'

fid = vj.inv.ResultFileReader(result_file_no_Raslip)
epochs = fid.epochs
rms = fid.rms_inland_at_epoch

plt.plot(epochs, rms, 'x-', label='no Raslip model')

# coupled model
result_file = '../../../run9/outs/nrough_06_naslip_11.h5'
fid = vj.inv.ResultFileReader(result_file)
epochs = fid.epochs
rms = fid.rms_inland_at_epoch

plt.plot(epochs, rms, 'o-', label='coupled model')

plt.xlabel('days after the mainshock')
plt.ylabel('RMS misfit (m)')
plt.legend(loc=0,prop={'size':10})
plt.savefig('mis_fit_comparison.png')
plt.show()
