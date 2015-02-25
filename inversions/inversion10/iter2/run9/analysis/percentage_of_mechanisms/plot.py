import numpy as np

import viscojapan as vj

partition_file = '../deformation_partition/deformation_partition.h5'
reader = vj.inv.DeformPartitionResultReader(partition_file)
Rco = reader.Rco
Raslip = reader.Raslip
d_added = reader.d_added
sites = reader.sites
sites = vj.sites_db.SitesDB().gets(sites)

day = 1300

rco = Rco.get_post_at_epoch(day)
raslip = Raslip.get_post_at_epoch(day)
d = d_added.get_post_at_epoch(day)

def get_mag(d):
    return np.sqrt(np.sum(d**2, axis=1))

rco_mag = get_mag(rco)
d_mag = get_mag(d)

z= abs(raslip[:,0])/abs(d[:,0])

plt = vj.gmt.applications.ZPlotter(sites, z)

plt.plot(clim=[-2,0])
plt.save('percentage.pdf')
