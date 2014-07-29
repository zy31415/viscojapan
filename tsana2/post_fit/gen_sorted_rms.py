import glob
import pickle
from os.path import join

import viscojapan as vj
      
rms_dic = vj.tsana.read_misfit_from_pickled_cfs('CFS_POST')

for cmpt in 'e', 'n', 'u':
    rms_sorted = vj.tsana.sort_by_misfit(rms_dic, cmpt)
    vj.tsana.save_to_file(rms_sorted, 'misfits/rms_sorted_by_%s'%cmpt)


