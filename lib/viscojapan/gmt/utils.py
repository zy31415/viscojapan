from os.path import normpath, join
import tempfile

import pGMT

from ..utils import get_this_script_dir

__all__=['plot_Tohoku_focal_mechanism', 'plot_slab_top',
         'plot_slab_contours', 'plot_slab','plot_vector_legend',
         'plot_plate_boundary', 'plot_etopo1', 'topo_cpts',
         'file_plate_boundary','file_kur_top','file_etopo1']

this_script_dir = get_this_script_dir(__file__)
file_kur_top = normpath(join(this_script_dir,
                             'share/kur_top.in'))
file_kur_contours = normpath(join(this_script_dir,
                              'share/kur_contours.in'))
file_plate_boundary = normpath(join(this_script_dir,
                              'share/PB2002_boundaries.gmt'))
topo_cpts = {
    'afrikakarte' : normpath(join(this_script_dir, 'share/afrikakarte.cpt')),
    'wiki-france' : normpath(join(this_script_dir, 'share/wiki-france.cpt')),
    'etopo1' : normpath(join(this_script_dir, 'share/ETOPO1.cpt')),
    }

file_etopo1 = '/home/zy/workspace/viscojapan/share/topo/ETOPO1_Bed_g_gmt4.grd'

def plot_Tohoku_focal_mechanism(gplt, scale=0.4, K='', O='',):
    text = tempfile.NamedTemporaryFile('w+t')
    text.write('''lon lat depth str dip slip st dip slip mant exp plon plat
    143.05, 37.52 20. 203 10 88 25 80 90  9.1 0 0 0
    ''')
    text.seek(0,0)
    gplt.psmeca(text.name,
                J='', R='',O=O,K=K,
                S='c%f'%scale,h='1')
    text.close()

def plot_slab_top(gplt):
    gplt.psxy(
        file_kur_top,
        J='', R='', O='', K='',
        W='thin, 50',
        )
    
def plot_slab_contours(gplt, file_contours=file_kur_contours):
    gplt.psxy(
        file_contours,
        J='', R='', O='', K='',
        Sq='L144/41.5/138/41.5:+Lh+ukm',
        W='thin, 50, --'
        )

def plot_slab(gplt, file_contours=file_kur_contours):
    plot_slab_top(gplt)
    plot_slab_contours(gplt, file_contours=file_contours)

def plot_vector_legend(gplt,lon,lat, text_offset_lon=0, text_offset_lat=0.1):
    # add scale vector
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f 2., 0.'%(lon, lat))
    text.seek(0,0)
    gplt.psvelo(
        text.name,
        J='', R='',O='',K='',
        A='0.07i/0.1i/0.1i+a45+g+e+jc',
        Sr='0.75/1/0',G='black',
        W='0.5, black',h='i',
        )
    text.close()

    # add label
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f 2m'%(lon+text_offset_lon, lat+text_offset_lat))
    text.seek(0,0)
    gplt.pstext(
        text.name,
        J='', R='',O='',K='',
        F='+f8+jLB',
        )
    text.close()

def plot_plate_boundary(gplt, color='red'):
    # plot plate boundary
    gplt.psxy(
        file_plate_boundary,
        R = '', J = '', O = '', K='', W='thick,%s'%color,
        Sf='0.25/3p', G='%s'%color)

def plot_etopo1(gplt, A='-70/20', file_topo_cpt=topo_cpts['afrikakarte']):
    gmt = pGMT.GMT()
    gmt.grdcut(
        file_etopo1,
        G = '~topo.grd',
        R = '')

    gmt = pGMT.GMT()
    gmt.grdgradient(
        '~topo.grd',
        G = '~topo_grad.grd',
        A = A,
        R = '')

    gplt.grdimage(
        '~topo.grd',
        J = '', C = file_topo_cpt,
        I = '~topo_grad.grd',
        O = '',K = '')

