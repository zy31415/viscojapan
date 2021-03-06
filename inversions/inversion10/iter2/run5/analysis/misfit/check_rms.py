import numpy as np

import viscojapan as vj

sites_2EXPs = [site.decode() for site in np.loadtxt('sites_2EXPs', '4a')]
sites_Yamagiwa = [site.decode() for site in np.loadtxt('sites_Yamagiwa', '4a')]

reader = vj.inv.DispResultReader('../../outs/nrough_05_naslip_11.h5')

sites = reader.sites

idx = [sites.index(site) for site in sites_Yamagiwa]
# rms = reader.get_cumu_rms(subset_sites = idx, subset_cmpt=[2])
rms = reader.get_cumu_rms(subset_cmpt=[2])
print(rms)
