#!/usr/bin/env python3
from subprocess import call

from pylab import *

tp=loadtxt('./sites.misfit','4a,f,')
sites=[ii[0].decode() for ii in tp]
for site in sites:
    call(['../fit_post.py','%s'%site,'-p'])

