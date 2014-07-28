from numpy import asarray, zeros_like

def cut_ts(t,tcuts):
    ''' Return logical indexing of epochs indicated by tcuts.
'''
    assert_tcuts_order(tcuts)
    ch = asarray(zeros_like(t),'bool')
    for cut in tcuts:
        t1=cut[0]
        t2=cut[1]
        ch |= ((t>t1) & (t<t2))
    return ch

def assert_tcuts_order(tcuts):
    for tcut in tcuts:
        assert tcut[0]<tcut[1]

    for tcut1, tcut2 in zip(tcuts[:-1], tcuts[1:]):
        assert tcut1[1] < tcut2[0]
        

def if_in_tcuts(t,tcuts):
    """ If t is in time intervals defined by tcuts.
If tcuts == None, return True.
t and tcuts used here are all in mjd format.
"""
    assert_tcuts_order(tcuts)
    if tcuts == None:
        return True
    t = asmjd(t)
    for tcut in tcuts:
        t1 = tcut[0]
        if t1 < inf and t1>-inf:
            t1 = asmjd(t1)
        t2 = tcut[1]
        if t2 < inf and t2 > -inf:
            t2 = asmjd(t2)
        if t>t1 and t<t2:
            return True
    return False

def if_in_tcuts_boundary(t,tcuts):
    """ If t is in time intervals defined by tcuts.
If tcuts == None, return True.
t and tcuts used here are all in mjd format.
"""
    assert_tcuts_order(tcuts)
    if tcuts == None:
        return True
    t1 = tcuts[0][0]
    t2 = tcuts[-1][1]
    if t>t1 and t<t2:
        return True
    return False
