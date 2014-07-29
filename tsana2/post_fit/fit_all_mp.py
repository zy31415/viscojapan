#!/usr/bin/env python3
from pylab import *
from os.path import join,exists
from os import remove
import time
import subprocess

tp=loadtxt('sites','4a')
sites=[ii.decode() for ii in tp]

_dir_postres='POSTRES'

from multiprocessing import Pool, cpu_count

def run(site):
    t1=time.time()

    fn=join(_dir_postres,'%s-post'%site)
    if exists(fn):
        print('Waring: file %s exists and skipped!'%fn)
    else:
        print('%s is running ...'%(site))
        fn_err='screenouts/%s.err'%site
        ferr=open(fn_err,'wt')
        fout=open('screenouts/%s.out'%site,'wt')
        rcode=subprocess.call(['./fit_post.py','%s'%site],stdout=fout,stderr=ferr)
        fout.close()
        ferr.close()

        if rcode==0:
            remove(fn_err)
            print('  %s is DONE in %f min'%(site,(time.time()-t1)/60.))
        else:
            print('  ERROR: %s, %f min'%(site,(time.time()-t1)/60.))

ncpus=5
#ncpus=5
p=Pool(ncpus)

p.map(run,sites)
