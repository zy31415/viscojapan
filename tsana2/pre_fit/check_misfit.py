import glob

from viscojapan.tsana import read_misfit_from_prelin_files, sort_by_misfit, save_to_file

def gen_sorted_misfit_files():
    files = glob.glob('linres/*')

    for kind in 'rms', 'std':
        sd_dic = read_misfit_from_prelin_files(files, kind)
        for cmpt in 'e', 'n', 'u':
            sd_sorted = sort_by_misfit(sd_dic, cmpt)
            save_to_file(sd_sorted, 'misfits/sorted_%s_%s'%(kind, cmpt))

gen_sorted_misfit_files()
