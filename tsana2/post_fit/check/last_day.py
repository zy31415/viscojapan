#!/usr/bin/env python3

import sys
sys.path.append('../../')
import utils

import glob

ts=[]
for f in glob.iglob('../../IGS08/*.IGS08.tenv'):
    t=utils.read_tenv_t(f,'mjd')
    print(t[-1])
