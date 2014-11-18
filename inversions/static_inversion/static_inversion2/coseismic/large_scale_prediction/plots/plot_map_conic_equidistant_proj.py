import pGMT
import tempfile
from subprocess import check_call

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = gmt.gplt

north = 80
south = 12
east = 200
west = 80
gplt.psbasemap(
    R = '80/200/12/80',       # region
    JD = '{lon0}/{lat0}/{lat1}/{lat2}/{wid}'\
    .format(lon0 = vj.TOHOKU_EPICENTER[0],
            lat0 = vj.TOHOKU_EPICENTER[1],
            lat1 = 12,
            lat2 = 8,
            wid = '9i',
            ), # projection
    B = '20', U='18/25/0',
    K = '')

# topo
#cpt = '../../share/topo/ETOPO1.cpt'
#vj.gmt.plot_etopo1(gplt)


# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,100,-.',
    W = 'faint,50',A='5000',Lf='155/15/35/500+lkm+jt',
    K = '',
    O = '')

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt, color='100')
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.2, K=None)

gmt.save('pred_hor_decay.pdf')

gmt.save_shell_script('shell.sh', output_file=' > out.ps')
