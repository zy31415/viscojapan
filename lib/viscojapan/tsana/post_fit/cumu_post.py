from numpy import asarray, nan, hstack, insert, arange, savetxt

t_eq = 55631

def get_cumu_post_cf(cf, post_model, t):
    global t_eq
    t = asarray(t)
    co = cf.get_subf('TOHOKU').jump

    if post_model =='EXP':
        f = cf.get_subf('EXP')
    elif post_model=='2EXPs':
        f = lambda t: cf.get_subf('EXP1')(t)+\
            cf.get_subf('EXP2')(t)
    else:
        raise ValueError('Post model not reconized.')

    res = f(t+t_eq)
    res += co
    return res

def get_cumu_post(cfs, t):
    t = asarray(t)
    pm = cfs.post_model
    res = []
    for cf, cmpt in zip(cfs, ('e', 'n', 'u')):
        assert cf.CMPT == cmpt
        res.append(get_cumu_post_cf(cf, pm, t).reshape([-1, 1]))
    res = hstack(res)
    if res.shape[1] == 2:
        res = insert(res, 2, nan,1)    
    return res

def save_cumu_post(cfs, days, cumu_post_file):
    ts = days
    cumu_post = get_cumu_post(cfs, ts)
    savetxt(cumu_post_file,
            hstack((ts.reshape([-1,1]), cumu_post)),
            fmt = '%4d  %f  %f  %f',
            header = 'days after mainshock || e_cumu (m) || n_cumu(m) || u_cumu(m)\n')
    
        
