import re

from numpy import loadtxt

def get_all_sites():
    tp=loadtxt(sites_file,'4a, 2f')
    return [ii[0] for ii in tp]

def get_sites_seafloor():
    ''' Seafloor sites name start with an understore "_"
'''
    with open(sites_file, 'rt') as fid:
        sites_seafloor = re.findall('^_.{3}', fid.read(),re.M)
    res = [si.encode() for si in sites_seafloor]
    return res



