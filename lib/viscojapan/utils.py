import os
from os.path import exists, isdir, dirname, realpath
from os import makedirs
import time
import shutil
import re

from numpy import hstack, asarray, frompyfunc
from numpy.random import normal

__all__ = ['delete_if_exists']

def delete_if_exists(fn):
    if os.path.exists(fn):
        if isdir(fn):
            shutil.rmtree(fn)
        else:
            os.remove(fn)

def create_dir_if_not_exists(path):
    if not exists(path):
        makedirs(path)

def get_this_script_dir(__file__):
    return dirname(realpath(__file__))


# assertions

def _assert_integer(var):
    assert isinstance(var, int), "%s is not an integer."%str(var)
    
def _assert_nonnegative_integer(var):
    _assert_integer(var)
    assert var >= 0, "%d is not non negative."%str(var)

def _assert_positive_integer(var):
    _assert_integer(var)
    assert var > 0, "%d is not positive."%str(var)

def _assert_file_not_exists(fn):
    assert not exists(fn), "File %s exist."%fn

def _assert_file_exists(fn):
    assert exists(fn), "File %s doesn't exist."%fn

def _assert_assending_order(l):
    assert all(l[i] <= l[i+1] for i in range(len(l)-1)) is True, \
           'The arr is not assending.'

def _assert_column_vector(res):
    sh = res.shape
    assert len(sh) ==2, "Wrong dimension. Must be column vector."
    assert sh[1] == 1, "Column number should 1."
    return sh[0]



# decorator:
class overrides:
    def __init__(self, super_class):
        self.super_class  = super_class
                
    def __call__(self, overrideing_method):
        assert(overrideing_method.__name__ in dir(self.super_class)), \
                "Overriding error. Can't find method '%s' in super class '%s'."%\
                (overrideing_method.__name__, self.super_class.__name__)
        
        return overrideing_method

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('''Summary:
Method : %r (%r, %r)
 Time  : %2.2f sec
 '''%(method.__name__, args, kw, te-ts))
        
        return result

    return timed

def my_vectorize(fn, arr):
    fn_vec = frompyfunc(fn, 1, 1)
    res = fn_vec(asarray(arr, float))
    return asarray(res, float)

def _find_section(ARR, val):
    _assert_assending_order(ARR)

    err = 1e-6
    
    assert val >= ARR[0] - err, '%f is out of upper edge'%val
    assert val <= ARR[-1] + err, '%f is out of lower edge'%val
    
    for nth, ai in enumerate(ARR[1:]):
        if val <= ai:
            break
        
    return nth + 1

def kw_init(self, kwargs):
    for name, value in kwargs.items():
        assert hasattr(self,name), 'Invalid key word arguments.'
        setattr(self,name, value)

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
