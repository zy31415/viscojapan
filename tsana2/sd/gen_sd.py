import numpy as np

from days_after_mainshock import days

import viscojapan as vj

sites = np.loadtxt('sites', '4a')

gen = vj.tsana.GenSD(
    dir_linres = '../pre_fit/linres/',
    sites = sites,
    days = days
    )

gen.save('sd.h5')
