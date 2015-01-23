import numpy as np
from pylab import plt

from viscojapan.tsana.post_fit.post import fit_post

import viscojapan as vj

site = 'ULAB'

pf = vj.tsana.PostFit(site)

cfs1 = pf.gen_cfs(cmpts='enu', post_model='EXP')
cfs1.go()
vj.tsana.plot_post(cfs1, ifshow=True)

cfs2 = pf.gen_cfs(cmpts='enu', post_model='2EXPs')
cfs2.go()
vj.tsana.plot_post(cfs2, ifshow=True)

print(cfs1.aic(), cfs2.aic())
dAIC = cfs2.aic() - cfs1.aic()

print(dAIC)

