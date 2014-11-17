import tempfile

import pGMT

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9'
           )

gplt = gmt.gplt

gplt.psbasemap(
    R = '125/133/33/39',       # region
    J = 'B129/36/33/39/15c', # projection
    B = '2', U='20/0/22/Yang', P='', K=''
    )

vj.gmt.plot_etopo1(gplt)

scale = 30

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, '../disp',scale)
plt_vec.plot_vectors()
plt_vec.plot_vec_legend(
    lon=131, lat=38.6,
    leg_len = 0.03,
    leg_txt = '3cm prediction',
    text_offset_lon = -0.3,
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'baek_2012/baek_2012_obs',scale,'red')
plt_vec.plot_vectors()
plt_vec.plot_vec_legend(
    lon=131, lat=38.2,
    leg_len = 0.03,
    leg_txt = '3cm observation',
    text_offset_lon = -0.3,
    )    

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    W = 'faint,100', L='f144/35.4/38/100+lkm+jt',
    O = '', K='')

#plot_horizontal_coseismic_vector(gplt)

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K=None)

gmt.save('pred_korea.pdf')
gmt.save_shell_script('shell.sh', output_file=' > out.ps')
