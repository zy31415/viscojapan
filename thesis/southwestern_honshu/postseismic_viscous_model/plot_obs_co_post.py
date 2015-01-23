from os.path import join
import numpy as np
import tempfile

import pGMT

import viscojapan as vj


gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9',
           'BASEMAP_TYPE','PLAIN',
           )

gplt = gmt.gplt

lon1 = 131.5
lon2 = 135.7
lat1 = 33
lat2 = 35.8

gplt.psbasemap(
    R = '{lon1}/{lon2}/{lat1}/{lat2}'.format(lon1=lon1,
                                     lon2=lon2,
                                     lat1 = lat1,
                                     lat2 = lat2
                                     ),       # region
    J = 'B{lon0}/{lat0}/{lat1}/{lat2}/18c'.format(
        lon0=(lon1+lon2)/2.,
        lat0 = (lat1+lat2)/2.,
        lat1 = lat1,
        lat2 = lat2), # projection
    B = '2', U='20/0/22/Yang', K=''
    )

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    G = 'lightblue2',
    O = '', K='')


scale = 15

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'post_1344_pred',scale)
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=135, lat=33.4,
    leg_len = 0.05,
    leg_txt = '5 cm prediction',
    text_offset_lon = 0,
    text_offset_lat = -0.06,
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'post_obs',scale,'red')
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=135, lat=33.2,
    leg_len = 0.05,
    leg_txt = '5 cm observation',
    text_offset_lon = 0,
    text_offset_lat = -0.06,
    )    

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    W = 'faint,100', L='f144/35.4/38/100+lkm+jt',
    O = '', K='')

#plot_horizontal_coseismic_vector(gplt)

vj.gmt.plot_focal_mechanism_JMA(gplt)

gplt.finish()
gmt.save('post_pred_obs.pdf')
