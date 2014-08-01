import glob
import pickle
from os.path import join

import viscojapan as vj
      
rms_dic = vj.tsana.read_misfit_from_pickled_cfs(
    glob.glob('CFS_POST/????-res.cfs'))

for cmpt in 'e', 'n', 'u':
    rms_sorted = vj.tsana.sorted_value(rms_dic, cmpt)
    vj.tsana.save_to_file(rms_sorted, 'check/sorted_rms_%s'%cmpt, 'rms')


