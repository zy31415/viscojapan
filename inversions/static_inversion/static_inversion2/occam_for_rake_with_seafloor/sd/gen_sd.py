from os.path import exists

import viscojapan as vj

sites = vj.Sites.init_from_txt('stations.in')

gen = vj.tsana.GenUniformOnshoreSDWithInfiniteSeafloorSD(
    sites = sites,
    days = [0],
    sd_co_hor = 1,
    sd_co_ver = 5,
    sd_post_hor = 1,
    sd_post_ver = 5
    )

file_sd_seafloor_inf = 'sd_seafloor_inf.h5'
if not exists(file_sd_seafloor_inf):
    gen.save(file_sd_seafloor_inf)

vj.tsana.copy_and_revise_sd_file(
    file_sd_seafloor_inf,
    'sites_seafloor',
    'sd_seafloor_.5.h5',
    (.5,.5,2.5)
    )

vj.tsana.copy_and_revise_sd_file(
    file_sd_seafloor_inf,
    'sites_seafloor',
    'sd_seafloor_01.h5',
    (1.,1.,5.)
    )
    
vj.tsana.copy_and_revise_sd_file(
    file_sd_seafloor_inf,
    'sites_seafloor',
    'sd_seafloor_02.h5',
    (2.,2.,10.)
    )

vj.tsana.copy_and_revise_sd_file(
    'sd_seafloor_inf.h5',
    'sites_seafloor',
    'sd_seafloor_04.h5',
    (4.,4.,20.)
    )
