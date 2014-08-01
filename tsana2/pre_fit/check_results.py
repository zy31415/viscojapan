import glob

from viscojapan.tsana.pre_fit.linres_reader import \
     read_sea, read_semi, read_rms, read_std
from viscojapan.tsana.check_results import collect_value, sorted_value, save_to_file

files = sorted(glob.glob('linres/*'))

for reader in read_sea, read_semi, read_rms, read_std:
    kind = reader.__name__.split('_')[1]
    print("Collecting and sorting value %s ..."%kind)
    val_dic = collect_value(files, reader)
    for cmpt in 'e', 'n', 'u':
        val_sorted = sorted_value(val_dic, cmpt)
        save_to_file(val_sorted, 'check/sorted_%s_%s'%(kind, cmpt), kind)
