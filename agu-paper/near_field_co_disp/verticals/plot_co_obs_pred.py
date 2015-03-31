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

lon1 = 139
lon2 = 145
lat1 = 34.7
lat2 = 41

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

# plot coseismic slip
splt = vj.gmt.GMTSlipPlotter(
    gplt = gplt,
    slip_file_txt = '../share/co_slip'
    )
splt.init(
#    original_cpt_file = 'bath_112.cpt',
    original_cpt_file = '../Blues_09.cpt',
    #if_cpt_reverse = True
          )
splt.plot_slip()
splt.plot_scale(
    xpos = 12,
    ypos = 5)

vj.gmt.plot_plate_boundary(gplt, color=100)

scale = 5
###########################
# onshore

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_ver_pred',scale)
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=142.5, lat=40.5,
    leg_len = 0.2,
    leg_txt = '20 cm pred.',
    text_offset_lon = -0.4,
    text_offset_lat = -0.15,
    if_vertical = True
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_ver_obs',scale,'red')
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=143.2, lat=40.5,
    leg_len = .2,
    leg_txt = '20 cm obs. ONSHORE',
    text_offset_lon = -0.2,
    text_offset_lat = -0.15,
    if_vertical = True,
    )    

#######################3
# plot seafloor:

scale = 1.5

# plot prediction
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_ver_pred_seafloor',scale)
plt_vec.plot_empty_vectors()
plt_vec.plot_vec_legend(
    lon=143, lat=35.2,
    leg_len = 1,
    leg_txt = '1 m pred.',
    text_offset_lon = -0.2,
    text_offset_lat = -0.25,
    if_vertical = True
    )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/co_ver_obs_seafloor',scale,'red')
plt_vec.plot_empty_vectors()
plt_vec.plot_vec_legend(
    lon=143.7, lat=35.2,
    leg_len = 1,
    leg_txt = '1 m obs. SEAFLOOR',
    text_offset_lon = -0.2,
    text_offset_lat = -0.25,
    if_vertical = True
    )    

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--', A='500',
    W = 'faint,100', L='f139.5/39.5/38/50+lkm+jt',
    O = '', K='')

vj.gmt.plot_seafloor_stations(gplt, marker_size=0, network='SEAFLOOR_POST',
                              justification='MB', text_offset_Y=0.03,
                              fontsize='8')

gplt.finish()

gmt.save('seafloor_co_ver_obs_pred.pdf')
    
