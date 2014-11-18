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
    JG = '{lon0}/{lat0}/{alt}/{azi}/{tilt}/{twist}/{Wid}/{Hei}/{wid}'\
    .format(lon0 = vj.TOHOKU_EPICENTER[0],
            lat0 = vj.TOHOKU_EPICENTER[1],
            alt = 2000,
            azi = 0,
            tilt = 0,
            twist = 0,
            Wid = 0,
            Hei = 0,
            wid = '4i',
            ), # projection
    B = '10g10', U='18/25/0',
    K = '')

# topo
#cpt = '../../share/topo/ETOPO1.cpt'
#vj.gmt.plot_etopo1(gplt)


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

gmt.save('pred_hor_decay.pdf')

gmt.save_shell_script('shell.sh', output_file=' > out.ps')
