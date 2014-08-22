import shutil
import glob
from os.path import join, basename

files = glob.glob('plots/nsd_09_*')

for file in files:
    shutil.copyfile(file,join('tmp/nsd_09/',basename(file)))
