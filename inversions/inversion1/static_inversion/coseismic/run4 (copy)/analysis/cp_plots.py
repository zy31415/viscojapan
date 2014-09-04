import shutil
import glob
from os.path import join, basename

files = glob.glob('../plots/nsd_??_rough_10_top_02.h5.pdf')

for file in files:
    shutil.copyfile(file,join('plots_slip/',basename(file)))
