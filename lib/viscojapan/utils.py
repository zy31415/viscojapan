import os
from os.path import exists
import time

from numpy import hstack
from numpy.random import normal

def delete_if_exists(fn):
    if os.path.exists(fn):
        os.remove(fn)

def get_this_script_dir(__file__):
    return os.path.dirname(os.path.realpath(__file__))
    
def gen_error_for_sites(num_sites,
                        east_st=6e-3, north_st=6e-3, up_st=20e-3):
    east_error = normal(0, east_st, (num_sites,1))
    north_error = normal(0, north_st, (num_sites,1))
    up_error = normal(0, up_st, (num_sites,1))
    error = hstack((east_error, north_error, up_error))
    error_flat = error.flatten().reshape([-1,1])
    return error_flat

# assertions

def _assert_integer(var):
    assert isinstance(var, int), "%s is not an integer."%str(var)
    
def _assert_nonnegative_integer(var):
    _assert_integer(var)
    assert var >= 0, "%d is not non negative."%str(var)

def _assert_not_exists(fn):
    assert not exists(fn), "File %s exist."%fn

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
