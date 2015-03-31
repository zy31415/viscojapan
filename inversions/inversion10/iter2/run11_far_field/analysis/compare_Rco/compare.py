import viscojapan as vj

def get_Rco(fn):
    partition_file = fn
    reader = vj.inv.DeformPartitionResultReader(partition_file)
    Rco = reader.Rco
    sites = reader.sites
    sites = vj.sites_db.SitesDB().gets(sites)
    return Rco, sites

Rco_coupled, sites = get_Rco('../deformation_partition/deformation_partition.h5')

Rco_no_Raslip, sites = get_Rco('../../../../../inversion_no_Raslip/model1_co+post/model1/run3/analysis/deformation_partition/deformation_partition.h5')

for day in 200, 1344:
    cmpt = 0

    r_coupled = Rco_coupled.get_post_at_epoch(day)[:,cmpt]
    r_no_raslip = Rco_no_Raslip.get_post_at_epoch(day)[:,cmpt]

    z = abs(r_coupled)/abs(r_no_raslip)
    
    plt = vj.gmt.applications.ZPlotter(sites, z)
    plt.plot(clim=[0,1], if_log=False, cpt_file='jet')
    plt.save('rco_coupled_over_no_aslip_day%04d_cmpt%d.pdf'%(day,cmpt))
