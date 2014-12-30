

import numpy  as np

import pGMT

import viscojapan as vj

res_file = '../../outs/nrough_06_naslip_11.h5'

reader = vj.inv.ResultFileReader(res_file)

rms_e = reader.get_rms_at_sites('e')
rms_n = reader.get_rms_at_sites('n')
rms_u = reader.get_rms_at_sites('u')

sites = reader.sites

plt = vj.gmt.ZPlotter(sites=sites, Z=rms_e)
plt.plot(clim=[-2.5,1.1])
plt.save('misfit.pdf')


