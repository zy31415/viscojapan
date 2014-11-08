import pGMT
import tempfile

import numpy as np

import viscojapan as vj

__doc__='''Observed Coseismic disp. This plot models Ozawa 2011.'''


def gen_coseismic_disp_file():
    reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
    co_disp = reader[0].reshape([-1,3])
    sites = vj.Sites([ii.decode() for ii in reader['sites']])

    text = tempfile.NamedTemporaryFile(mode='w+t')
    _text = '# lon lat x y * * * name of station\n'
    for ci, site in zip(co_disp, sites):
        _text += '%f %f %f %f 0. 0. 0. %s\n'%\
                 (site.lon, site.lat, ci[0], ci[1], site.name)
    text.write(_text)
    text.seek(0,0)
    return text

def plot_horizontal_coseismic_vector(gplt):
    text = gen_coseismic_disp_file()
    gplt.psvelo(
        text.name,
        J='', R='',O='',K='',
        A='0.07i/0.1i/0.1i+a45+g+e',
        Sr='0.6/1/0',G='black',
        W='0.5, black',h='i',
        )
    text.close()

    vj.gmt.plot_vector_legend(gplt, lon=143.6, lat=35.9,
                       text_offset_lon = 0.25,
                       text_offset_lat = 0.08)
    

def gen_coseismic_vertical_file():
    reader = vj.EpochalFileReader('../../tsana/post_fit/cumu_post.h5')
    co_disp = reader[0].reshape([-1,3])
    # print(np.max(co_disp[:,2]))
    sites = vj.Sites([ii.decode() for ii in reader['sites']])

    text = tempfile.NamedTemporaryFile(mode='w+t')
    _text = '# lon lat vertical\n'
    for ci, site in zip(co_disp, sites):
        _text += '%f %f %f \n'%\
                 (site.lon, site.lat, ci[2])
    text.write(_text)
    text.seek(0,0)
    return text

def plot_vertical_coseismic_disp(gplt):
    text = gen_coseismic_vertical_file()
    gmt = pGMT.GMT()
    gmt.nearneighbor(
        text.name,
        G='~ver.grd', I='1k', N='8', R='', S='60k'
        )
    gplt.grdimage(
        '~ver.grd',
        J='', R='', C='vertical_disp.cpt',O='',K=''
        )

    text.close()
    # fill water with white color
    gplt.pscoast(R='', J='', S='white', O='', K='')
       
    

######################################
gmt = pGMT.GMT()
gmt.gmtset('ANNOT_FONT_SIZE_PRIMARY','9',
           'LABEL_FONT_SIZE','9'
           )

gplt = pGMT.GMTPlot()

gplt.psbasemap(
    R = '138/145/35/42',       # region
    J = 'B141.5/38.5/35/42/15c', # projection
    B = '2:.Oberved coseismic disp:', U='20/0/22/Yang', P='', K=''
    )

plot_vertical_coseismic_disp(gplt)

vj.gmt.plot_slab(gplt, file_contours='../../share/slab1.0/kur_contours_above_100km.in')

gplt.pscoast(
    R = '', J = '',
    D = 'h', N = 'a/faint,50,--',
    W = 'faint,100', L='f144/35.4/38/100+lkm+jt',
    O = '', K='')

plot_horizontal_coseismic_vector(gplt)

vj.gmt.plot_Tohoku_focal_mechanism(gplt,K='')

gplt.psscale(
    D='1.4/14c/4c/.2c',
    Baf='::/:m:', O='',
    C='vertical_disp.cpt')

gplt.save('coseismic_disp.pdf')
gplt.save_shell_script('shell.sh', output_file=' > out.ps')
