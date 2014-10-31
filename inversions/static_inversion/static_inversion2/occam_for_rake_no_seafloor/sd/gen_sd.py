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

gen.save('sd_seafloor_inf.h5')
