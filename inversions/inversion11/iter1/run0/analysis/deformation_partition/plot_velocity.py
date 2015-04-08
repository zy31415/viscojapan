import viscojapan as vj

from pylab import plt

partition_file = './deformation_partition.h5'
#result_file = '../../outs/best_result.h5'

reader = vj.inv.DeformPartitionResultReader(partition_file)
Rco = reader.Rco
Raslip = reader.Raslip
Ecumu = reader.Ecumu
D = reader.d_added

site = 'ULAB'
cmpt = 'e'

vel_rco = Rco.vel_ts(site, cmpt) * 365*1000
vel_raslip = Raslip.vel_ts(site, cmpt) * 365*1000
vel_ecumu = Ecumu.vel_ts(site, cmpt) * 365*1000
vel_d = D.vel_ts(site, cmpt) * 365*1000
epochs = Rco.get_epochs()[1:]

plt.plot(epochs, vel_rco, label='vel Rco')
plt.plot(epochs, vel_raslip, label='vel Raslip')
plt.plot(epochs, vel_ecumu, label='vel Ecumu')
plt.plot(epochs, vel_d, label='vel D added')
plt.legend()
plt.grid('on')
plt.ylabel('mm/yr')
plt.xlabel('days after the main shock')
plt.show()
