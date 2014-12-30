import numpy as np

tp = np.loadtxt('disp_cmpts/total','4a,1a, 21f')
total = np.asarray([ii[2] for ii in tp])
total_post = (total - total[:,0:1])[:,1:]
site_cmpts = ['%s %s'%(ii[0].decode(), ii[1].decode()) for ii in tp]

tp = np.loadtxt('disp_cmpts/elastic','4a,1a, 21f')
elastic = np.asarray([ii[2] for ii in tp])
elastic_post = (elastic - elastic[:,0:1])[:,1:]


tp = np.loadtxt('disp_cmpts/Rco','4a,1a, 21f')
Rco = np.asarray([ii[2] for ii in tp])[:,1:]

tp = np.loadtxt('disp_cmpts/Raslip','4a,1a, 21f')
Raslip = np.asarray([ii[2] for ii in tp])[:,1:]

print(Raslip.shape)

_total_post = elastic_post + Rco + Raslip

ch1 = (elastic_post*_total_post>0)
ch2 = (Rco*_total_post>0)
ch3 = (Raslip*_total_post>0)
mask = (ch1 & ch2 & ch3)

def compute_percentage(part, total):
    percentage = abs(part)/abs(total)
    percentage[~mask] = np.nan
    return percentage

percentage_elastic = compute_percentage(elastic_post, _total_post)
percentage_Rco = compute_percentage(Rco, _total_post)
percentage_Raslip = compute_percentage(Raslip, _total_post)

def save_file(fn, arr):
    with open(fn,'wt') as fid:
        for site_cmpt, ln  in zip(site_cmpts, arr):
            fid.write('%s '%site_cmpt)
            for ii in ln:
                fid.write('%5.3f '%ii)
            fid.write('\n')

save_file('disp_cmpts/percentage_elastic', percentage_elastic)
save_file('disp_cmpts/percentage_Rco', percentage_Rco)
save_file('disp_cmpts/percentage_Raslip', percentage_Raslip)
