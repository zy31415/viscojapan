from os.path import join
import collections
import sqlite3

import numpy as np
import pyproj as pj
import simplekml as sk

from .site import Site
from ..sites_db import get_pos_dic, get_networks_dic

__all__=['Sites', 'save_sites_to_txt',
         'save_sites_to_kml']

def _is_Site(self, obj):
    assert isinstance(obj, Site), 'Must be Site object.'

class Sites(collections.UserList):
    def __init__(self, *args, **kwargs):
        for ii in args[0]:
            _is_Site(ii)

        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        _is_Site(value)
        super().__setitem__(key, value)


def save_sites_to_txt(sites, fn,
                      format='id name lon lat',
                      header=None):
    with open(fn, 'wt') as fid:
        if header is not None:
            fid.write(header)
            if header[-1] != '\n':
                fid.write('\n')                
        fid.write('# ' + format +'\n')
        formats = format.split()
        for site in sites:
            for fm in formats:
                val = getattr(site, fm)
                fid.write('{val}  '.format(val=val))
            fid.write('\n')
                
def save_sites_to_kml(sites, fn, label_color='red', icon_name='flag'):
    kml = sk.Kml()
    for site in sites:
        pnt = kml.newpoint(name = site.name)
        pnt.coords = [(site.lon, site.lat)]
        pnt.style.labelstyle.color = get_kml_color(label_color)
        pnt.style.iconstyle.icon.href = get_kml_icon_link(icon_name)
        pnt.description = get_kml_html_description(site)
    kml.save(fn)

def get_kml_color(label_color):
    if label_color == 'red':
        out = sk.Color.red
    else:
        raise NotImplementedError('Not recongnized color.')
    return out

def get_kml_icon_link(icon_name):
    ''' Fetch icon link.
Check all the icons here:
https://sites.google.com/site/gmapsdevelopment/
'''
    if icon_name == 'flag':
        out  = 'http://maps.google.com/mapfiles/kml/pal4/icon21.png'
    elif icon_name == 'down_arrow':
        out  = 'http://maps.google.com/mapfiles/kml/pal4/icon20.png'        
    else:
        raise NotImplementedError('Not recongnized icon name.')
    return out

def get_kml_html_description_for_onshore(site):
    description = '''<![CDATA[
<a href="http://geodesy.unr.edu/NGLStationPages/stations/{id}.sta">
    {name} ({id})</a>
<br>
<img src="http://geodesy.unr.edu/tsplots/IGS08/TimeSeries/{id}.png">
]]>'''.format(id=site.id, name=site.name)
    return description

def get_kml_html_description_for_seafloor(site):
    description = '''<![CDATA[
Seafloor station:  {name}{id} <br>
<br>
]]>'''.format(id=site.id, name=site.name)
    return description


def get_kml_html_description(site):
    if site.if_onshore:
        description = get_kml_html_description_for_onshore(site)
    elif site.if_seafloor:
        description = get_kml_html_description_for_seafloor(site)
    else:
        raise NotImplementedError()
    return description
