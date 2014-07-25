from numpy import asarray, zeros_like

def cut_ts(t,tcuts):
    ''' Return logical indexing of epochs indicated by tcuts.
'''
    ch = asarray(zeros_like(t),'bool')
    for cut in tcuts:
        t1=cut[0]
        t2=cut[1]
        ch = ch | ((t>t1) & (t<t2))
    return ch
