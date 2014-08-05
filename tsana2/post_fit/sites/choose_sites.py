#!/usr/bin/env python3
from pylab import *

import sys
sys.path.append('..')
from utils import *
from date_utils import *
import datetime

tp=loadtxt('../pre/sites','4a')
sites1=[ii.decode() for ii in tp]

def remove_ill_sites(sites):
    tp=loadtxt('sites.ill','4a')
    try:
        tp[0][0]
    except:
        tp=[bytes(tp)]
    illsites=[ii.decode() for ii in tp]
    outsites=[]
    for site in sites:
        if site in illsites:
            continue
        else:
            outsites.append(site)
    return outsites

# remove problematic stations
sites1=remove_ill_sites(sites1)



    
    
