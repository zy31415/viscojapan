import re
import os

import numpy as np

import viscojapan as vj

sites = np.loadtxt('sites/sites', '4a',usecols=(0,))
sites = [site.decode() for site in sites]
        
vj.tsana.gen_vel_and_vsd_file('linres/',sites, 'pre_vel')
