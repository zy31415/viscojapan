#!/usr/bin/env python3
from pylab import *
from os import remove
from os.path import join,exists
import time
import subprocess

import argparse
parser = argparse.ArgumentParser(description='Do linear fit for all stations.')
parser.add_argument('-n',dest='ncpus', type=int, required=True,
                   help='Number of cpus.')
args = parser.parse_args()

_dir_linres='linres'

from multiprocessing import Pool, cpu_count

def run(par):
    t1=time.time()

    fn=join(_dir_linres,'%s.lres'%par)
    if exists(fn):
        print('Waring: file %s exists and skipped!'%fn)
    else:
        print('%s is running ...'%(par))
        site,cmpt=par.split('.')
        fn_err='stderr/%s'%par
        ferr=open(fn_err,'wt')
        fout=open('stdout/%s'%par,'wt')
        rcode=subprocess.call(['./fit-lin-sh.py',
                               '-s','%s'%site,
                               '-c','%s'%cmpt,
                               '-v'],
                              stdout=fout,stderr=ferr)
        ferr.close()
        fout.close()
        
        if rcode==0:
            remove(fn_err)
            print('  %s is DONE in %f min'%(site,(time.time()-t1)/60.))
        else:
            print('  ERROR: %s, %f min'%(site,(time.time()-t1)/60.))

tp=loadtxt('../raw_ts/sites','4a,2f')
sites=[ii[0].decode() for ii in tp]

pars=[]
for site in sites:
    for cmpt in 'enu':
        pars.append('%s.%s'%(site,cmpt))

ncpus=args.ncpus

print(ncpus)

p=Pool(ncpus)
p.map(run,pars)

