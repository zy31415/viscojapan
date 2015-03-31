from os.path import join
import numpy as np
import tempfile

import pGMT

import viscojapan as vj


def plot(
    disp_file1,
    disp_file2,
    outf,
    leg1='',
    leg2='',
    color1 = 'black',
    color2 = 'red',
    ):
    gmt = pGMT.GMT()
    gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
               'LABEL_FONT_SIZE','9',
               'BASEMAP_TYPE','PLAIN',
               )

    gplt = gmt.gplt

    lon1 = 133.5
    lon2 = 135.1
    lat1 = 34.5
    lat2 = 35.5

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
        B = '.5', U='20/0/22/Yang', K=''
        )

    gplt.pscoast(
        R = '', J = '',
        D = 'h', N = 'a/faint,50,--', A='500',
        G = 'lightblue2',
        O = '', K='')

    scale = 27

    # plot disp file1
    plt_vec = vj.gmt.VecFieldPlotter(gmt, disp_file1,scale, color1)
    plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                         pen_width='1.2')
    plt_vec.plot_vec_legend(
        lon=135, lat=33.4,
        leg_len = 0.05,
        leg_txt = leg1,
        text_offset_lon = 0,
        text_offset_lat = -0.06,
        )

    # plot disp file2
    plt_vec = vj.gmt.VecFieldPlotter(gmt, disp_file2,scale, color2)
    plt_vec.plot_vectors(arrow_width='.2', head_length='.1', head_width='.1',
                         pen_width='1.2')
    plt_vec.plot_vec_legend(
        lon=135, lat=33.2,
        leg_len = 0.05,
        leg_txt = leg2,
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
    gmt.save(outf)


plot('share/co_obs', 'share/post_1344_obs', 'co_post_obs.pdf',
     leg1='5cm coseismic obs.',
     leg2='5cm postseismic obs.',
     color1 = 'red',
     color2 = 'black'
     )
plot('share/co_obs', 'share/co_pred', 'co_obs_pred.pdf',
     leg1 = '5cm coseismic obs.',
     leg2 = '5cm coseismic pred.',
     color1 = 'red',
     color2 = 'black'
     )
plot('share/post_1344_obs', 'share/post_1344_pred_slip_only', 'post_obs_pred_slip_only.pdf',
     leg1 = '5cm postseismic obs.',
     leg2 = '5cm afterslip-only pred.',
     color1 = 'red',
     color2 = 'black'
     )
plot('share/post_1344_obs', 'share/post_1344_pred_coupled', 'post_obs_pred_coupled.pdf',
     leg1 = '5cm postseismic obs.',
     leg2 = '5cm coupled model pred.',
     color1 = 'red',
     color2 = 'black'
     )

