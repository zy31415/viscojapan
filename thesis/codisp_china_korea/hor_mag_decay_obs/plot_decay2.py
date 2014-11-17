import pGMT
import tempfile
from subprocess import check_call

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6')

gplt = gmt.gplt

gplt.psbasemap(
    R = '95/160/12/55',       # region
    JB = '127.5/33.5/12/55/19c', # projection
    B = '10g10', U='18/25/0',
    K = '')

# topo
#cpt = '../../share/topo/ETOPO1.cpt'
vj.gmt.plot_etopo1(gplt)

pltxyz = vj.gmt.GMTXYZ(
    gmt,
    file_xyz = 'obs_hor_mag',
    if_log_color_scale = True,
    cpt_scale = '-3/0.6/0.001',
    workdir = '~tmp',
    interp_inc = '20k',
    interp_searching_radius = '800+k',
    )
pltxyz.maskout_water(A='1000k',D='h')
pltxyz.plot_xyz()
pltxyz.plot_contour(
    contours=[0.003,0.005,0.01,0.1,2],
    W='thick,red',
    label_font_size = 8,
    )
pltxyz.plot_scale(x=15, y=8)

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
    K = '',
    O = '')

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt, color='100')
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.2, K=None)

gmt.save('obs_hor_decay.pdf')

gmt.save_shell_script('shell.sh', output_file=' > out.ps')
