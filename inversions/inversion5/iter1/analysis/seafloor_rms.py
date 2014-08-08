import glob

import numpy as np

import viscojapan as vj

tp = np.loadtxt('../../sd_seafloor/seafloor_sd','4a,d, 3f')
sites_seafloor = [ii[0].decode() for ii in tp]
days = [ii[1] for ii in tp]

ed_obs = vj.EpochalDisplacement('../../cumu_post_with_seafloor.h5')

for site, epoch in zip(sites_seafloor, days):
    for cmpt in 'e','n','u':
        print(ed_obs.get_epoch_value_at_site(site, cmpt,epoch))

files = glob.glob('outs_epochal_pred_disp/ano_??_bno_10.h5')
file = files[0]


ed_obs = vj.EpochalDisplacement()
