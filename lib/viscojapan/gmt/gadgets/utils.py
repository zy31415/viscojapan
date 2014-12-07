import tempfile

import pGMT

from ...utils import get_this_script_dir
from ...sites_db import get_pos_dic_of_a_network
from ...fault_model import FaultFileReader

from ..share import file_kur_top, file_kur_contours,\
     file_plate_boundary, file_etopo1, topo_cpts

__all__=['plot_slab_top',
         'plot_slab_contours', 'plot_slab','plot_vector_legend',
         'plot_plate_boundary', 'plot_etopo1', 
         'plot_seafloor_stations', 'plot_fault_model',
         'plot_GEONET_Japan_stations']


def plot_slab_top(gplt,
                  K='',
                  color= '50',
                  lw='thin'):
    gplt.psxy(
        file_kur_top,
        J='', R='', O='', K=K,
        W='%s,%s'%(lw, color),
        )
    
def plot_slab_contours(gplt, file_contours=file_kur_contours,
                       K='',
                       color='50',
                       lw='thin',
                       label_line = '144/41.5/138/41.5',
                       label_font_size = '9',
                       label_color = 'black',
                       if_contour_annotation = True,
                       ):
    if if_contour_annotation:
        Sq = 'L%s:+Lh+ukm+f%s,%s'%(label_line, label_font_size,label_color)
    else:
        Sq = None
        
    gplt.psxy(
        file_contours,
        J='', R='', O='', K=K,
        Sq = Sq,
        W='%s,%s,--'%(lw, color)
        )

def plot_slab(gplt, file_contours=file_kur_contours,
              K='', color='50', lw='thin',
              label_line = '144/41.5/138/41.5',
              label_font_size = '9',
              label_color = 'balck',
              if_contour_annotation = True
              ):
    plot_slab_top(gplt, K='', color=color, lw=lw)
    plot_slab_contours(gplt, file_contours=file_contours,
                       K=K, color=color, lw=lw,
                       label_line=label_line,
                       label_font_size = label_font_size,
                       label_color = label_color,
                       if_contour_annotation = if_contour_annotation)

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

def plot_plate_boundary(gplt,
                        color='red',
                        lw = 'thick',
                        gap = '0.25',
                        ms = '3p',
                        K=''):
    # plot plate boundary
    gplt.psxy(
        file_plate_boundary,
        R = '', J = '', O = '', K=K,
        W='%s,%s'%(lw, color),
        Sf='%s/%s+r+b'%(gap, ms),
        G='%s'%color)

def plot_etopo1(gplt, A='-70/20', file_topo_cpt=topo_cpts['afrikakarte']):
    gmt = pGMT.GMT()

    file_topo_cut = tempfile.NamedTemporaryFile()
    gmt.grdcut(
        file_etopo1,
        G = file_topo_cut.name,
        R = '')

    gmt = pGMT.GMT()
    file_topo_grad = tempfile.NamedTemporaryFile()
    gmt.grdgradient(
        file_topo_cut.name,
        G = file_topo_grad.name,
        A = A,
        R = '')

    gplt.grdimage(
        file_topo_cut.name,
        J = '', C = file_topo_cpt,
        I = file_topo_grad.name,
        O = '',K = '')

    # close temporary files:
    file_topo_cut.close()
    file_topo_grad.close()

def plot_stations(gplt, network, S, color, fill_color,
                  lw='thick'):
    tp = get_pos_dic_of_a_network(network)
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, pos in tp.items():
            fid.write('%f %f %s\n'%(pos[0], pos[1], site))
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            S = S,
            R = '', J = '', O='' ,K='' ,W='%s,%s'%(lw,color),
            G=fill_color)

def plot_seafloor_stations(gplt, marker_size=0.5, color='red',
                           lw='thick'):
    plot_stations(gplt, 'SEAFLOOR',
                  S = 's%f'%marker_size,
                  color = color,
                  fill_color = 'white',
                  lw=lw
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
    
