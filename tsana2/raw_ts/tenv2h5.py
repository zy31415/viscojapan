#!/usr/bin/env python3
''' Read tenv files and convert to h5 database.
05/27/2014
'''

from glob import iglob
from pylab import *
from h5py import File
import datetime

_ts_data_type=dtype("a4,a7,f,i,i,i,3f,f,3f,f,f")

fh5=File('igs08.h5','w')

num_site=1
for f in iglob('./IGS08/*'):
    site=f.split('/')[-1].split('.')[-3]
    #print(site)
    print(f)
    tp=loadtxt(f,_ts_data_type)
    if size(tp)<=1:
        continue
    
    mjd=asarray([ii[3] for ii in tp])

    e=asarray([ii[6][0] for ii in tp])
    n=asarray([ii[6][1] for ii in tp])
    u=asarray([ii[6][2] for ii in tp])

    esd=asarray([ii[8][0] for ii in tp])
    nsd=asarray([ii[8][1] for ii in tp])
    usd=asarray([ii[8][2] for ii in tp])
    
    fh5['%s/t'%site]=mjd
    fh5['%s/t'%site].attrs['unit']='mjd'
    
    fh5['%s/e'%site]=e
    fh5['%s/e'%site].attrs['unit']='meter'
    
    fh5['%s/n'%site]=n
    fh5['%s/n'%site].attrs['unit']='meter'
    
    fh5['%s/u'%site]=u
    fh5['%s/u'%site].attrs['unit']='meter'
    
    fh5['%s/esd'%site]=esd
    fh5['%s/esd'%site].attrs['unit']='meter'
    
    fh5['%s/nsd'%site]=nsd
    fh5['%s/nsd'%site].attrs['unit']='meter'
    
    fh5['%s/usd'%site]=usd
    fh5['%s/usd'%site].attrs['unit']='meter'

    num_site+=1

fh5['/'].attrs['Date created']=str(datetime.datetime.today())
fh5['/'].attrs['# of sites']=num_site
fh5.close()

