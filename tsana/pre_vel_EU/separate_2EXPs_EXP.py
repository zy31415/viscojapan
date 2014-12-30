import re

import numpy as np

def match(model):
    with open('../config/postmodel') as fid:
        matches = re.findall(r".*\s%s"%model, fid.read(), re.M)
    sites = [ii[:4] for ii in matches]
    return sites


sites_2EXPs = match('2EXPs')
sites_EXP = match('EXP')


sites = sites_2EXPs

def pick_lines(sites, fn):
    with open('share/pre_vel_EU.gmt','r') as fid:
        txt = fid.read()

    out = []
    for site in sites:
        matches = re.findall(r".*%s"%site, txt)
        if len(matches) != 1:
            continue
        out.append(matches[0])

    with open(fn,'wt') as fid:
        fid.write('\n'.join(out))
            
pick_lines(sites_2EXPs, 'share/pre_vel_2EXPs.gmt')
pick_lines(sites_EXP, 'share/pre_vel_EXP.gmt')
