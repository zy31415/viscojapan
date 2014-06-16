import os
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
