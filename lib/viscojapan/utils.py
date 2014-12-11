import os
from os.path import exists, isdir, dirname, realpath
from os import makedirs
import time
import shutil
import re

import numpy as np
from numpy import hstack, asarray, frompyfunc
from numpy.random import normal
import pyproj

__all__ = ['delete_if_exists',
           'assert_integer','assert_nonnegative_integer',
           'assert_col_vec_and_get_nrow',
           'assert_square_array_and_get_nrow',
           'assert_descending_order','assert_assending_order',
           'assert_strictly_descending_order','assert_strictly_assending_order',
           'get_this_script_dir','next_non_commenting_line',
           'merge_disp_dic','make_grids','as_string',
           'get_middle_point','pop_from_center']

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

def assert_integer(var):
    assert isinstance(var, int), "%s is not an integer."%str(var)
    
def assert_nonnegative_integer(var):
    assert_integer(var)
    assert var >= 0, "%d is not non negative."%str(var)

def assert_positive_integer(var):
    assert_integer(var)
    assert var > 0, "%d is not positive."%str(var)

def assert_file_not_exists(fn):
    assert not exists(fn), "File %s exist."%fn

def assert_file_exists(fn):
    assert exists(fn), "File %s doesn't exist."%fn

def assert_strictly_assending_order(l):
    assert all(l[i] < l[i+1] for i in range(len(l)-1)) is True, \
           'The arr is not strictly assending.'

def assert_assending_order(l):
    assert all(l[i] <= l[i+1] for i in range(len(l)-1)) is True, \
           'The arr is not assend.'

def assert_strictly_descending_order(l):
    assert all(l[i] > l[i+1] for i in range(len(l)-1)) is True, \
           'The arr is not strickly descending.'
    
def assert_descending_order(l):
    assert all(l[i] >= l[i+1] for i in range(len(l)-1)) is True, \
           'The arr is not descending.'
    
def assert_col_vec_and_get_nrow(res) -> int:
    sh = res.shape
    assert len(sh) ==2, "Wrong dimension. Must be column vector."
    assert sh[1] == 1, "Column number should 1."
    return sh[0]

def assert_square_array_and_get_nrow(arr) -> int:
    assert isinstance(arr, np.ndarray)
    assert len(arr.shape) == 2
    assert arr.shape[0] == arr.shape[1]
    return arr.shape[0]

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
    assert_assending_order(ARR)

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

def merge_disp_dic(dic1, dic2):
    out = dic1.copy()
    for key, val in dic2.items():
        if key not in out:
            out[key] = val
        else:
            out[key] = (out[key] + val)/2.
    return out

def make_grids(north, south, west, east, dx, dy):
    assert north > south
    assert west < east
    g = pyproj.Geod(ellps='WGS84')

    lats = [south]
    
    while lats[-1]<north:
        lon, lat, _ = g.fwd(west, lats[-1],0,dy)
        lats.append(lat)

    grids = []
    
    for lat in lats:
        lons = [west]
        while lons[-1] < east:
            lon, lat, _ = g.fwd(lons[-1], lat, 90, dx)
            while lon < 0:
                lon += 360.
            lons.append(lon)
            grids.append((lon, lat))

    return grids
            
def as_string(input):
    if isinstance(input, str):
        return input
    if isinstance(input, bytes):
        return input.decode()
    return [as_string(ii) for ii in input]

def get_middle_point(x):
    x1 = (x[:-1,:] + x[1:,:])/2.
    x2 = (x1[:,:-1] + x1[:,1:])/2.
    return x2    

def pop_from_center(center, arr1, arr2):
    assert len(center) ==2
    idx = []
    for ith in range(len(arr1)):
        for jth in range(len(arr2)):
            idx.append((ith, jth))
    idx_sorted = sorted(idx, key=lambda x : np.sqrt((x[0]-center[0])**2+(x[1]-center[1])**2))

    idx1_sorted = [ii[0] for ii in idx_sorted]
    idx2_sorted = [ii[1] for ii in idx_sorted]

    arr1_sorted = arr1[idx1_sorted]
    arr2_sorted = arr2[idx2_sorted]

    for idx1, idx2 in zip(idx1_sorted, idx2_sorted):
        yield(idx1, arr1[idx1], idx2, arr2[idx2])
