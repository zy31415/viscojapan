import pGMT
import tempfile

import numpy as np

import viscojapan as vj

def plot(infile, outfile,
         if_log_color_scale,
         cpt_scale,
         contours,
         scale_interval,
         ):    
    gmt = pGMT.GMT()
    gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
               'LABEL_FONT_SIZE','9',
               'COLOR_NAN','white',
               'COLOR_BACKGROUND','white',
               'COLOR_FOREGROUND','white'
               )

    gmt.gplt.psbasemap(
        R = '128/148/30/46',       # region
        J = 'B138/38/30/46/16c', # projection
        B = '4',
        U='20/0/25/Yang', P='', K=''
        )

    plt_ver = vj.gmt.GMTXYZ(
        gmt,
        infile,
        cpt_scale = cpt_scale,
        if_log_color_scale = if_log_color_scale,
        )
    plt_ver.plot_xyz()
    plt_ver.plot_scale(scale_interval='1')
    plt_ver.plot_contour(contours = contours, W='thick')

    vj.gmt.plot_plate_boundary(gmt.gplt,color='150')

    gmt.gplt.pscoast(
        R = '', J = '',
        D = 'h', N = 'a/faint,50,--',
        W = 'faint,100', L='f145/31/38/200+lkm+jt',
        O = '', K='')

    vj.gmt.plot_Tohoku_focal_mechanism(gmt.gplt,K=None)

    gmt.save(outfile)
    gmt.gplt.save_shell_script('shell.sh', output_file=' > out.ps')

plot('../pred_vertical_abs','codisp_ver_abs.pdf',
     cpt_scale = '-4/-0.15/0.01',
     if_log_color_scale = True,
     contours = [0.001,0.004, 0.01,0.1],
     scale_interval= 1.
     )

