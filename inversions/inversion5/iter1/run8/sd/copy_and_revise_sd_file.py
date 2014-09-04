import numpy as np

from viscojapan.tsana import copy_and_revise_sd_file

copy_and_revise_sd_file(
    '../../../../../tsana/sea_floor/sd_uniform_co.h5',
    'seafloor_sd',
    'sd_uniform_co.h5',
    [200]*3)
