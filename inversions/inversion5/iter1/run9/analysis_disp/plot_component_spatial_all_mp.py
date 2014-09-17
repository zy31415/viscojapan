import subprocess
import multiprocessing
import glob
from os.path import join, basename

import numpy as np

from epochs_log import epochs

files = glob.glob('disp_cmpts/percentage_*')

def func(args):
    file = args[0]
    nepoch = args[1]
    ncmpt = args[2]
    bn = basename(file)
    print(bn, nepoch, ncmpt)
    of1 = 'plots_component_spatial/%s_nepoch_%d_ncmpt_%d.png'%(bn, nepoch, ncmpt)
    of2 = 'plots_component_spatial/%s_nepoch_%d_ncmpt_%d.pdf'%(bn, nepoch, ncmpt)
    subprocess.check_call(['python3', 'plot_component_percentage_spatial.py'
                           ,file, '-nepoch','%d'%nepoch,
                           '-ncmpt','%d'%ncmpt,
                           '-o', of1, of2])

if __name__ == '__main__':
    args = []
    for file in files:
        for nepoch in range(19):
            for ncmpt in range(3):
                args.append((file, nepoch, ncmpt))
    nproc = 4
    pool = multiprocessing.Pool(nproc)
    pool.map(func, args)
