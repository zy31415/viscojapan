from os.path import join
import numpy as np
import tempfile

import pGMT

import viscojapan as vj


slip_file_txt = '_inverted_slip.txt'
cpt_file = 'Blues_09.cpt'

gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'BASEMAP_TYPE','PLAIN',
           )

gplt = gmt.gplt

lon1 = 138
lon2 = 146
lat1 = 33.5
lat2 = 42


gplt.psbasemap(
    R = '{lon1}/{lon2}/{lat1}/{lat2}'.format(lon1=lon1,
                                     lon2=lon2,
                                     lat1 = lat1,
                                     lat2 = lat2
                                     ),       # region
    J = 'B{lon0}/{lat0}/{lat1}/{lat2}/14c'.format(
        lon0=(lon1+lon2)/2.,
        lat0 = (lat1+lat2)/2.,
        lat1 = lat1,
        lat2 = lat2), # projection
    B = '2', U='20/0/22/Yang', K='', P=''
    )

out_grd = '~grd'

gmt.nearneighbor(
    slip_file_txt,
    G = out_grd, I='1k', N='8', R='', S='35k'
    )

gmt.makecpt(
    C=cpt_file,
    T = '-0.1/2.1/.01',
    D='o',
    Z=''
    )
   
gmt.save_stdout('~cpt')

gplt.grdimage(
    out_grd, J='', R='',
    C = '~cpt',
    O='',K='', G='', Q=''
    )


vj.gmt.plot_plate_boundary(gplt, color=100)

gplt.psscale(
    R='', J='', O = '', K='',
    C = '~cpt',
    D='12/5/3/.2',
    B='1::/:m:',
    )

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    W = 'faint,100', L='f144.5/34/38/100+lkm+jt',
    O = '', K='')


gplt.finish()

gmt.save('_inverted_slip.pdf')
