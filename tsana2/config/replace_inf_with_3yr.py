import re

with open('linsec_inf', 'rt') as fid:
    new = re.sub('-INF', '08JAN01', fid.read())

with open('linsec_3yr', 'wt') as fid:
    fid.write(new)
    
