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
    
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print('%r (%r, %r) %2.2f sec' % \
              (method.__name__, args, kw, te-ts))
        return result

    return timed

def _assert_integer(var):
    assert isinstance(var, int), "%s is not an integer."%str(var)
    
def _assert_nonnegative_integer(var):
    _assert_integer(var)
    assert var >= 0, "%d is not non negative."%str(var)

def _assert_not_exists(fn):
    assert not exists(fn), "File %s exist."%fn

def gen_error_for_sites(num_sites,
                        east_st=6e-3, north_st=6e-3, up_st=20e-3):
    east_error = normal(0, east_st, (num_sites,1))
    north_error = normal(0, north_st, (num_sites,1))
    up_error = normal(0, up_st, (num_sites,1))
    error = hstack((east_error, north_error, up_error))
    error_flat = error.flatten().reshape([-1,1])
    return error_flat
