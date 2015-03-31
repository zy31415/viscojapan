import tempfile

import pGMT
import viscojapan as vj


gmt = pGMT.GMT()

gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'FONT_ANNOT_PRIMARY','6',
           'MAP_FRAME_TYPE','plain')

gplt = gmt.gplt

gplt.psbasemap(
    R = '128/145/30/44',       # region
    JB = '136.5/37/37/44/16c', # projection
    B = '5', U='18/25/0',
    P='',K='',
    )

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,150,-.',
    W = 'faint,dimgray',A='500',L='142/32/38/200+lkm+jt',
    O = '', K='')

lon1 = 133.5
lon2 = 135.1
lat1 = 34.5
lat2 = 35.5
points = [(lon1,lat1),(lon2,lat1),(lon2, lat2),(lon1, lat2)]
vj.gmt.plot_polygon(gplt, points,
                    lw='4')


vj.gmt.plot_focal_mechanism_JMA(gplt, scale=.2, fontsize=0)

gplt.finish()
gmt.save('location.pdf')
