import os
from os.path import exists
import time

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
