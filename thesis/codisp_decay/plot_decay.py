import pGMT
import tempfile

import viscojapan as vj

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6')
gmt.gmtset('COLOR_NAN','white',
           'COLOR_BACKGROUND','white',
           'COLOR_FOREGROUND','white'
           )

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '95/160/12/55',       # region
    JB = '127.5/33.5/12/55/19c', # projection
    B = '10g10', U='18/25/0',
    K = '')

# magnitude
gmt = pGMT.GMT()

gmt.nearneighbor(
    'horizontal_disp_mag',
    G='~hor_mag.grd', I='30k', N='8', R='', S='1000+k'
    )

gmt = pGMT.GMT()
gmt.makecpt(C='seminf-haxby.cpt',T='-3/.6/0.1',Q='',M='')
gmt.save_stdout('~hor_mag.cpt')

gplt.grdimage(
    '~hor_mag.grd',
    J='', R='', C='~hor_mag.cpt',O='',K=''
    )

# fill water with white color
gplt.pscoast(R='', J='', S='white', O='', K='')

# plot coast
gplt.pscoast(
    R = '', J = '',
    D = 'l', N = 'a/faint,100,-.',
    W = 'faint,50',A='1000',Lf='155/15/35/500+lkm+jt',
    K = '',
    O = '')

gplt.psscale(
    D='0.3/12.5/4c/.2c',
    Baf='::/:m:', O='',K='',
    C='~hor_mag.cpt',Q='')

# plot plate boundary
vj.gmt.plot_plate_boundary(gplt, color='100')
vj.gmt.plot_Tohoku_focal_mechanism(gplt,scale=0.2, K=None)

gplt.save('hor_deczy.pdf')

gplt.save_shell_script('shell.sh', output_file=' > out.ps')
