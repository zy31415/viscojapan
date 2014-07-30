#!/usr/bin/env python3
''' This script sort the sites file.
'''
import re
import datetime
from tempfile import NamedTemporaryFile
from numpy import loadtxt
import shutil
import os

with open('sites','r') as fid:
    tp=re.findall('^#.*',fid.read(),re.M)

sites=loadtxt('sites','4a')
sites=sorted(sites)

fid=NamedTemporaryFile('r+',delete=False)
fid.write('\n'.join(tp))
fid.write('\n#\n# sorted by sort_sites.py on %s\n'%(datetime.datetime.now()))
for site in sites:
    fid.write('%s\n'%(site.decode()))
name=fid.name
fid.close()

shutil.copyfile(name,'sites')
os.remove(name)
