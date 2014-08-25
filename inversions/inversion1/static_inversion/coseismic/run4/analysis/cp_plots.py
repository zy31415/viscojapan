import shutil
import glob
from os.path import join, basename

nsd=9

files = glob.glob('../plots/nsd_%02d_*'%nsd)

for file in files:
    shutil.copyfile(file,join('nsd_%02d/'%nsd,basename(file)))
