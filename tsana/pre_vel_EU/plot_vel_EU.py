import pGMT

import viscojapan as vj

gmt = pGMT.GMT()

gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = gmt.gplt

gplt.psbasemap(
    R = '128/147/30/46',       # region
    JB = '137.5/38.5/35/41.5/14c', # projection
    B = '5', U='18/25/0',
    P='',K='',
    )

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,150,-.',
    W = 'faint,dimgray',A='500',L='144/32/38/200+lkm+jt',
    O = '', K='')

# plot 2EXPs
plt = vj.gmt.VecFieldPlotter(
    gmt = gmt,
    vec_file = 'share/pre_vel_2EXPs.gmt',
    scale = .01,
    color = 'red',
    )

plt.plot_vectors(arrow_width = '0.03i')

# plot EXP
plt = vj.gmt.VecFieldPlotter(
    gmt = gmt,
    vec_file = 'share/pre_vel_EXP.gmt',
    scale = .01
    )

plt.plot_vectors(arrow_width = '0.03i')
plt.plot_vec_legend(
    lon = 143.5,
    lat = 33,
    leg_len = 50,
    leg_txt = '50 cm',
    text_offset_lon = -.2,
    text_offset_lat = .2
    )

vj.gmt.plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

gplt.finish()
gmt.save('pre_vel_EU.pdf')
