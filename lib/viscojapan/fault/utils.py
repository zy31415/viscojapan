from numpy import asarray, frompyfunc

from ..utils import _assert_assending_order

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
