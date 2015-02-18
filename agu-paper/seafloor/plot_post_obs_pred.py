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

if_pred = False
if_pred = True

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

if if_pred:
    # plot coseismic slip
    splt = vj.gmt.GMTSlipPlotter(
        gplt = gplt,
        slip_file_txt = 'share/co_slip'
        )
    splt.init(
    #    original_cpt_file = 'bath_112.cpt',
        original_cpt_file = 'Blues_09.cpt',
        #if_cpt_reverse = True
              )
    splt.plot_slip()
    splt.plot_scale(
        xpos = 12,
        ypos = 7)

    # plot postseismic slip
    splt = vj.gmt.GMTSlipPlotter(
        gplt = gplt,
        slip_file_txt = 'share/aslip_1344',
        )
    splt.init()
    splt.plot_slip_contour(
        contours=[2,3,4,5],
        W='2'
        )

vj.gmt.plot_plate_boundary(gplt, color=100)

scale = 0.8
###########################
# onshore

if if_pred:
    # plot prediction
    plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_1344_pred',scale)
    plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                         pen_width='1.2')
    plt_vec.plot_vec_legend(
        lon=143.5, lat=40.8,
        leg_len = 1,
        leg_txt = '1 m pred. ONSHORE',
        text_offset_lon = -0.2,
        text_offset_lat = -0.11,
        )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_obs',scale,'red')
plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                     pen_width='1.2')
plt_vec.plot_vec_legend(
    lon=143.5, lat=40.5,
    leg_len = 1,
    leg_txt = '1 m obs. ONSHORE',
    text_offset_lon = -0.2,
    text_offset_lat = -0.11,
    )    

#######################3
# plot seafloor:

scale = 4

if if_pred:
    # plot prediction
    plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_1344_pred_seafloor',scale)
    plt_vec.plot_empty_vectors()
    plt_vec.plot_vec_legend(
        lon=143.7, lat=35.7,
        leg_len = .4,
        leg_txt = '40 cm pred. SEAFLOOR',
        text_offset_lon = -0.2,
        text_offset_lat = -0.18,
        )

# plot observation
plt_vec = vj.gmt.VecFieldPlotter(gmt, 'share/post_obs_seafloor',scale,'red')
plt_vec.plot_empty_vectors()
plt_vec.plot_vec_legend(
    lon=143.7, lat=35.2,
    leg_len = .4,
    leg_txt = '40 cm obs. SEAFLOOR',
    text_offset_lon = -0.2,
    text_offset_lat = -0.18,
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

if not if_pred:
    gmt.save('seafloor_post_obs_only.pdf')
else:
    gmt.save('seafloor_post_obs_pred.pdf')
    
