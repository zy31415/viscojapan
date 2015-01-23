import re

__all__ = ['get_sec']

def get_sec(file_sec, site, dtype='mjd'):
    ''' Read time sections from time section file.
'''
    with open(file_sec) as fid:
        linsecs=re.findall('^\s*%s.*'%site,fid.read(),re.M)
    out=[]
    for li in linsecs:
        tp=li.split()
        t1=tp[1]
        t2=tp[2]
        if t1.upper()=='-INF':
            t1=-inf
        else:
            t1=asdtype(t1,dtype)
        if t2.upper()=='INF' or t2.upper()=='+INF':
            t2=inf
        else:
            t2=asdtype(t2,dtype)
        out.append((t1,t2))
    return out
