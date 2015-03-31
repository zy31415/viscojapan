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

for day in 200, 1344:
    rco = Rco.get_velocity_at_epoch(day)
    raslip = Raslip.get_velocity_at_epoch(day)
    r = rco + raslip
    easlip = Ecumu.get_velocity_at_epoch(day)
    d = d_added.get_velocity_at_epoch(day)

    cmpt = 0

    z_easlip_over_r = abs(easlip[:,cmpt])/abs(r[:,cmpt])
    z_raslip_over_rco = abs(raslip[:,cmpt]/rco[:,cmpt])

    plt = vj.gmt.applications.ZPlotter(sites, z_easlip_over_r)
    plt.plot(clim=[0,.5], if_log=False, cpt_file='jet')
    plt.save('plots/easlip_over_rtotal_vel_day%04d_cmpt%d.pdf'%(day,cmpt))
