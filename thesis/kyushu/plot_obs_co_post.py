import tempfile

import pGMT

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9'
           )

gplt = gmt.gplt

gplt.psbasemap(
    R = '95/140/20/55',       # region
    J = 'B117.5/37.5/20/55/15c', # projection
    B = '5', U='20/0/22/Yang', P='', K=''
    )

vj.gmt.plot_etopo1(gplt)

scale = 50

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'china_pred.in',scale)
plt_vec.plot_vectors()
plt_vec.plot_vec_legend(
    lon=130, lat=23,
    leg_len = 0.01,
    leg_txt = '1cm prediction',
    text_offset_lon = -1,
    text_offset_lat = -1,
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'china_obs.in',scale,'red')
plt_vec.plot_vectors()
plt_vec.plot_vec_legend(
    lon=130, lat=25,
    leg_len = 0.01,
    leg_txt = '1cm observation',
    text_offset_lon = -1,
    text_offset_lat = 1,
    )    

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    W = 'faint,100', L='f144/35.4/38/100+lkm+jt',
    O = '', K='')

#plot_horizontal_coseismic_vector(gplt)

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K=None)

gmt.save('pred_china.pdf')
gmt.save_shell_script('shell.sh', output_file=' > out.ps')
