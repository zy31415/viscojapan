from os.path import normpath, join
import tempfile

import pGMT

from ..utils import get_this_script_dir
from ..sites_db import get_pos_dic_of_a_network
from ..fault_model import FaultFileReader


__all__=['plot_slab_top',
         'plot_slab_contours', 'plot_slab','plot_vector_legend',
         'plot_plate_boundary', 'plot_etopo1', 'topo_cpts',
         'file_plate_boundary','file_kur_top','file_etopo1',
         'plot_seafloor_stations', 'plot_fault_model',
         'plot_GEONET_Japan_stations']

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
    'seminf-haxby' : normpath(join(this_script_dir, 'share/seminf-haxby.cpt')),
    }

file_etopo1 = '/home/zy/workspace/viscojapan/share/topo/ETOPO1_Bed_g_gmt4.grd'

def plot_slab_top(gplt):
    gplt.psxy(
        file_kur_top,
        J='', R='', O='', K='',
        W='thin,50',
        )
    
def plot_slab_contours(gplt, file_contours=file_kur_contours):
    gplt.psxy(
        file_contours,
        J='', R='', O='', K='',
        Sq='L144/41.5/138/41.5:+Lh+ukm',
        W='thin,50,--'
        )

def plot_slab(gplt, file_contours=file_kur_contours):
    plot_slab_top(gplt)
    plot_slab_contours(gplt, file_contours=file_contours)

def plot_vector_legend(gplt,
                       legend_len , scale,
                       lon, lat,
                       text_offset_lon=0, text_offset_lat=0.1):
    # add scale vector
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f %f 0.'%(lon, lat, legend_len))
    text.seek(0,0)
    gplt.psvelo(
        text.name,
        J='', R='',O='',K='',
        A='0.07i/0.1i/0.1i+a45+g+e+jc',
        Sr='%f/1/0'%scale,G='black',
        W='0.5,black',h='i',
        )
    text.close()

    # add label
    text = tempfile.NamedTemporaryFile(mode='w+t')
    text.write('%f %f %.1fm'%(lon+text_offset_lon, lat+text_offset_lat,legend_len))
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

def plot_stations(gplt, network, S, color, fill_color):
    tp = get_pos_dic_of_a_network(network)
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, pos in tp.items():
            fid.write('%f %f %s\n'%(pos[0], pos[1], site))
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            S = S,
            R = '', J = '', O='' ,K='' ,W='thick,%s'%color,
            G=fill_color)

def plot_seafloor_stations(gplt, marker_size=0.5, color='red'):
    plot_stations(gplt, 'SEAFLOOR',
                  S = 's%f'%marker_size,
                  color = color,
                  fill_color = 'white'
                  )
    
def plot_GEONET_Japan_stations(gplt, marker_size=0.05, color='red'):
    plot_stations(gplt, 'GEONET',
                  S = 'c%f'%marker_size,
                  color = color,
                  fill_color = color)

def plot_fault_model(gplt, file_fault):
    reader = FaultFileReader(file_fault)
    lats = reader.LLats
    lons = reader.LLons
    with tempfile.NamedTemporaryFile('w+t') as fid:
        _plot_fault_model_write_multisegment_file(lons, lats, fid)                
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            R = '', J = '', O='' ,K='' ,W='thick,red')
        
def _plot_fault_model_write_multisegment_file(lons, lats, fid):
    for lon, lat in zip(lons, lats):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))
    for lon, lat in zip(lons.T, lats.T):
        fid.write('>\n')
        for loni, lati in zip(lon, lat):
            fid.write('%f %f\n'%(loni, lati))
    
