#!/usr/bin/env python3
from pylab import *
from os.path import join,exists
from os import remove
import time
import subprocess

import argparse
parser = argparse.ArgumentParser(description='Do post fit for all stations.')
parser.add_argument('-n',dest='ncpus', type=int, required=True,
                   help='Number of cpus.')
args = parser.parse_args()

tp=loadtxt('sites/sites','4a')
sites=[ii.decode() for ii in tp]

_dir_postres='pots_res'

from multiprocessing import Pool, cpu_count

def run(site):
    t1=time.time()

    fn=join(_dir_postres,'%s-post'%site)
    if exists(fn):
        print('Waring: file %s exists and skipped!'%fn)
    else:
        print('%s is running ...'%(site))
        fn_err='stderr/%s'%site
        ferr=open(fn_err,'wt')
        fout=open('stdout/%s'%site,'wt')
        rcode=subprocess.call(['./fit-post.py','%s'%site],stdout=fout,stderr=ferr)
        fout.close()
        ferr.close()

        if rcode==0:
            remove(fn_err)
            print('  %s is DONE in %f min'%(site,(time.time()-t1)/60.))
        else:
            print('  ERROR: %s, %f min'%(site,(time.time()-t1)/60.))

ncpus = args.ncpus
print('# CPU: %d'%ncpus)
p=Pool(ncpus)

p.map(run,sites)
