import numpy  as np

import pGMT

import viscojapan as vj

res_file = '../../outs/nrough_06_naslip_11.h5'

ana = vj.inv.DispAnalyser(res_file)

rms_cumu_e = ana.get_cumu_rms(subset_cmpt = [True, False, False],
                         axis = 0)
rms_cumu_n = ana.get_cumu_rms(subset_cmpt = [False, True, False],
                         axis = 0)
rms_cumu_u = ana.get_cumu_rms(subset_cmpt = [False, False, True],
                         axis = 0)

rms_post_e = ana.get_post_rms(subset_cmpt = [True, False, False],
                         axis = 0)
rms_post_n = ana.get_post_rms(subset_cmpt = [False, True, False],
                         axis = 0)
rms_post_u = ana.get_post_rms(subset_cmpt = [False, False, True],
                         axis = 0)

sites = ana.result_file_reader.sites

plt = vj.gmt.ZPlotter(sites=sites, Z=rms_post_e)
plt.plot(clim=[-2.5,1.1])
plt.save('misfit.pdf')


