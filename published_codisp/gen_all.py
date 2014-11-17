import numpy as np


def merge_disp_dic(dic1, dic2):
    out = dic1.copy()
    for key, val in dic2.items():
        if key not in out:
            out[key] = val
        else:
            out[key] = (out[key] + val)/2.
    return out

def read_disp_file(fn):
    tp = np.loadtxt(fn,'4a, f, f')
    return {ii[0].decode():np.asarray((ii[1],ii[2]),float)
            for ii in tp}
    
   
baek = read_disp_file('Baek_2012/baek_2012_obs')
zhao = read_disp_file('Zhao_2012/zhao_2012_obs')
wang = read_disp_file('Wang_2011/wang_2011_obs')

china = merge_disp_dic(wang,zhao)
all_disp = merge_disp_dic(baek, china)

with open('china_codisp','wt') as fid:
    for k, v in china.items():
        fid.write('%s %f %f\n'%(k,v[0],v[1]))

with open('all_published_codisp','wt') as fid:
    for k, v in all_disp.items():
        fid.write('%s %f %f\n'%(k,v[0],v[1]))
