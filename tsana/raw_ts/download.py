#!/usr/bin/env python3
''' This script downloads tenv files through website.
'''
from pylab import *
from subprocess import *

tp=loadtxt('sites/sites','4a')
sites=[ii[0] for ii in tp]

link='wget -P IGS08/ http://geodesy.unr.edu/gps_timeseries/tenv/IGS08/{}.IGS08.tenv'

for site in sites:
    print(site)
    check_call(link.format(site.decode()),shell=True)
