import numpy as np

import viscojapan as vj

sites1 = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',
                                          cmpt_code=6,
                                          post_model='2EXPs')
sites2 = vj.tsana.get_sites_according_to_postmodel('../../../config/postmodel',
                                          cmpt_code=7,
                                          post_model='2EXPs')
sites_ = sites1 + sites2

sites_have_post =  np.loadtxt('../../sites/sites','4a',usecols=(0,))

sites = list(set(sites_) & set(sites_have_post))



with open('sites_2EXPs','w') as fid:
    fid.write('''# sites the postseismic disp. of which are estimated using Model 2EXPs.
# num of sites: %d
# 
'''%(len(sites)))

    for site in sorted(sites):
        fid.write('%s\n'%site.decode())
