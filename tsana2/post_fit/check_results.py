import glob

from viscojapan.tsana.post_fit.post_res_reader import read_rms, collect_value
from viscojapan.tsana import sorted_value, save_to_file
files = glob.glob('post_res/????.post')

rms_dic = collect_value(files, read_rms)
for cmpt in 'e', 'n', 'u':
    rms_sorted = sorted_value(rms_dic, cmpt)
    save_to_file(rms_sorted, 'check/sorted_rms_%s'%cmpt, 'rms')
