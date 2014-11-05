import numpy as np

def _get_num_records(fn):
    with open(fn,'rt') as fid:
        for ln in fid:
            if ln.strip()[0]!='#':
                return len(ln.split())-2
            
def load_array(fn):
    n = _get_num_records(fn)
    tp = np.loadtxt(fn, '4a,1a,%df'%n)
    return np.asarray([ii[2] for ii in tp])
