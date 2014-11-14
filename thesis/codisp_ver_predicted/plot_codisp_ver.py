import pGMT
import tempfile

import numpy as np

import viscojapan as vj


gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'COLOR_NAN','white',
           'COLOR_BACKGROUND','white',
           'COLOR_FOREGROUND','white'
           )

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '128/148/30/46',       # region
    J = 'B138/38/30/46/16c', # projection
    B = '4',
    U='20/0/25/Yang', P='', K=''
    )

plt_ver = vj.gmt.GMTXYZ(gplt, 'pred_vertical')
plt_ver.plot_xyz()
plt_ver.plot_scale()

vj.gmt.plot_plate_boundary(gplt,color='150')

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--',
    W = 'faint,100', L='f145/31/38/200+lkm+jt',
    O = '', K='')

##text = gen_codisp_ver_file()
##gmt = pGMT.GMT()
##gmt.nearneighbor(
##    text.name,
##    G='~ver.grd', I='1k', N='8', R='', S='60k'
##    )
##text.close()
##with tempfile.NamedTemporaryFile('w+t') as fid:
##    fid.write('''
##0 A
##''')
##    fid.seek(0,0)
##    gplt.grdcontour(
##        '~ver.grd', C=fid.name, A='1+f9+um',
##        G='n1/.5c', J='', R='', O='',K=''
##        )

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K=None)

gplt.save('codisp_ver.pdf')
gplt.save_shell_script('shell.sh', output_file=' > out.ps')
