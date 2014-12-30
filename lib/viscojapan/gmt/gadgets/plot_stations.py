import tempfile

import pGMT

from ...sites_db import get_pos_dic_of_a_network, get_true_name_by_id, get_pos

__all__ = ['plot_stations', 'plot_seafloor_stations', 'plot_GEONET_Japan_stations']

def plot_stations(gplt, sites, S, color, fill_color,

                  lw='thick',
                  fontsize = None,
                  fontcolor = 'black',
                  justification = 'RT',
                  text_offset_X = 0,
                  text_offset_Y = 0,
                  ):
    lons, lats = get_pos(sites)
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, lon, lat in zip(sites, lons, lats):
            site = get_true_name_by_id(site)
            fid.write('%f %f %s\n'%(lon, lat, site))
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            S = S,
            R = '', J = '', O='' ,K='' ,W='%s,%s'%(lw,color),
            G=fill_color)
        
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, lon, lat in zip(sites, lons, lats):
            site = get_true_name_by_id(site)
            fid.write('%f %f %s\n'%(lon+text_offset_X,
                                    lat+text_offset_Y,
                                    site))
        fid.seek(0,0)
        if fontsize is not None:
            gplt.pstext(fid.name,
                        R='', J='', O='', K='',
                        F='+f{fontsize},{fontcolor}+a0+j{justification}'.\
                        format(fontsize = fontsize,
                               fontcolor = fontcolor,
                               justification = justification)
                        )

def plot_seafloor_stations(gplt, marker_size=0.5, color='red',
                           lw='thick',
                           fontsize='6',
                           network='SEAFLOOR',
                           justification = 'RT',
                           text_offset_X = 0,
                           text_offset_Y = 0,
                           ):
    sites = get_pos_dic_of_a_network(network).keys()
    plot_stations(
        gplt, sites,
        S = 's%f'%marker_size,
        color = color,
        fill_color = 'white',
        lw=lw,
        fontsize = fontsize,
        justification = justification,
        text_offset_X = text_offset_X,
        text_offset_Y = text_offset_Y
        )
    
def plot_GEONET_Japan_stations(gplt, marker_size=0.05, color='red',
                               fontsize=None):
    sites = get_pos_dic_of_a_network('GEONET').keys()
    plot_stations(
        gplt, sites,
        S = 'c%f'%marker_size,
        color = color,
        fill_color = color,
        fontsize = fontsize,
        )
