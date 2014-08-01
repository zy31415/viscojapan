#!/usr/bin/env python3
from pylab import *
''' This file generate the station file.
'''
sites=loadtxt('sites2','4a')

tp=loadtxt('llh','4a,3f')
pos={ii[0]:ii[1] for ii in tp}

with open('sites','wt') as fid:
    fid.write('''# The file is generated on 10 Apr, 2014.
# Number of stations is %d.
# Downloading of time series is following this list.
#
# site lon lat
'''%(len(sites)))
    for site in sites:
        p=pos[site]
        fid.write('%s %f %f\n'%(site.decode(),p[0],p[1]))
         
