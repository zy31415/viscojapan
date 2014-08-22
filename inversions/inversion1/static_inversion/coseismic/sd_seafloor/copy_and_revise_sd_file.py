import numpy as np

from viscojapan.tsana import copy_and_revise_sd_file

for nsd, sd in enumerate(np.linspace(0.0001, 0.05, 10)):
    copy_and_revise_sd_file(
        '../../../../../tsana/sea_floor/sd_with_seafloor.h5',
        'seafloor_sd',
        'sd_files/sd_with_seafloor_%02d.h5'%nsd,
        [sd]*3)
    
