#!/usr/bin/env python3
from pylab import *
from os.path import exists
sites=loadtxt('../sites','4a')

for site in sites:
    assert exists('../CFS_POST/%s-res.cfs'%site.decode()),sitels
    
