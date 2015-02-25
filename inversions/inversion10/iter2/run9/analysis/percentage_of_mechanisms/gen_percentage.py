import numpy as np

import viscojapan as vj

partition_file = '../deformation_partition/deformation_partition.h5'

reader = vj.inv.DeformPartitionResultReader(partition_file)
Rco = reader.Rco
d_added = reader.d_added
sites = reader.sites
sites = vj.sites_db.SitesDB().gets(sites)

rco = Rco.get_post_at_epoch(1300)
d = d_added.get_post_at_epoch(1300)

def get_mag(d):
    return np.sqrt(np.sum(d**2, axis=1))

rco_mag = get_mag(rco)
d_mag = get_mag(d)

with open('mag_percentage.txt','w') as fid:
    for s, pi in zip(sites, rco_mag/d_mag):
        fid.write('%f %f %f %s\n'%(s.lon, s.lat, pi, s.id))
