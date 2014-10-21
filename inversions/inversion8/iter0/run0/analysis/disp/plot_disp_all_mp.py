import subprocess
import multiprocessing

import numpy as np

tp = np.loadtxt('./disp_cmpts/total','4a,')
sites = sorted(list(set([ii[0].decode() for ii in tp])))

def func(site):
    print(site)
    subprocess.check_call(['python3', 'plot_disp.py',site,
                           '-o', 'plots_disp/%s.png'%site, 'plots_disp/%s.pdf'%site])

if __name__ == '__main__':
    nproc = 8
    pool = multiprocessing.Pool(nproc)
    pool.map(func, sites)
    
     
