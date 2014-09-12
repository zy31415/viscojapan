import numpy as np

from viscojapan.tsana import copy_and_revise_sd_file

copy_and_revise_sd_file(
    'sd_ozawa.h5',
    'seafloor_sd',
    'sd_ozawa_seafloor.h5',
    [20]*3)
