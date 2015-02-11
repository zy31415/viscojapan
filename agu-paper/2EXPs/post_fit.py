import pickle

import viscojapan as vj

site = 'J550'

fit = vj.tsana.PostFit(site=site)
cfs = fit.gen_cfs(cmpts='enu', post_model='EXP')
cfs.go()

with open('%s_EXP.pkl'%site, 'wb') as fid:
    pickle.dump(cfs, fid)


fit = vj.tsana.PostFit(site=site)
cfs = fit.gen_cfs(cmpts='enu', post_model='2EXPs')
cfs.go()

with open('%s_2EXPs.pkl'%site, 'wb') as fid:
    pickle.dump(cfs, fid)
