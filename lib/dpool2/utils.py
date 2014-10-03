from os.path import exists

import numpy as np
import psutil as ps

def _assert_file_exists(fn):
    assert exists(fn), "File %s doesn't exist."%fn

# iterate text file
def if_line_is_commenting(ln):
    tp = ln.strip()
    if len(tp)==0:
        return True
    if tp[0] == '#':
        return True
    return False

def next_non_commenting_line(fid):
    for ln in fid:
        if not if_line_is_commenting(ln):
            yield ln

def free_cpu(interval=0.1, ntimes=20):
    cpu_percents = []
    for n in range(ntimes):
        cpu_percents.append(ps.cpu_percent(interval=interval))
    cpu_percent = np.mean(cpu_percents)
    ncpu = ps.cpu_count()
    free_cpu_num = ncpu * (1. - cpu_percent/100.)
    return free_cpu_num
