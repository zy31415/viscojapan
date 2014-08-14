import numpy as np

from viscojapan.tsana import copy_and_revise_sd_file

sd = 0.001

copy_and_revise_sd_file(
    '../../../../../tsana/sea_floor/sd_with_seafloor.h5',
    'seafloor_sd',
    'sd_with_seafloor.h5',
    [sd]*3)
    
