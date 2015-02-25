import numpy as np

import viscojapan as vj

partition_file = '../deformation_partition/deformation_partition.h5'
reader = vj.inv.DeformPartitionResultReader(partition_file)
Rco = reader.Rco
Raslip = reader.Raslip
Ecumu = reader.Ecumu
d_added = reader.d_added
sites = reader.sites
sites = vj.sites_db.SitesDB().gets(sites)

day = 200

rco = Rco.get_post_at_epoch(day)
raslip = Raslip.get_post_at_epoch(day)
ecumu = Ecumu.get_post_at_epoch(day)
d = d_added.get_post_at_epoch(day)

def get_mag(d):
    return np.sqrt(np.sum(d**2, axis=1))

rco_mag = get_mag(rco)
d_mag = get_mag(d)

cmpt = 0

for mech in 'raslip', 'rco', 'ecumu':
    z= abs(locals()[mech][:,cmpt])/abs(d[:,cmpt])
    plt = vj.gmt.applications.ZPlotter(sites, z)
    plt.plot(clim=[0,1], if_log=False, cpt_file='jet')
    plt.save('plots/ercentage_east_%s_day%04d_cmpt%d.pdf'%(mech, day,cmpt))
