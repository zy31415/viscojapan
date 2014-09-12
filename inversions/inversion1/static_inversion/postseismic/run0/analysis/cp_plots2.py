import shutil
import glob
from os.path import join, basename


files = glob.glob('../plots/nsd_??_rough_08_top_02*')

for file in files:
    shutil.copyfile(file,join(basename(file)))
