from os.path import join

import numpy as np
import pyproj as pj
import simplekml as sk

import viscojapan as vj

import sqlite3
from ..sites_db import get_pos_dic, get_networks_dic

__all__=['read_sites_from_txt', 'save_sites_to_txt',
         'save_sites_to_kml']

def read_sites_from_txt(fn):
    sites = np.loadtxt(fn, '4a', usecols=(0,))
    return [Site(ii.decode()) for ii in sites]

def save_sites_to_txt(sites, fn, header=None):
    with open(fn, 'wt') as fid:
        if header is not None:
            fid.write(header)
            if header[-1] != '\n':
                fid.write('\n')                
        fid.write('# site lon lat\n')
        for site in self:
            fid.write('%s %f %f \n'%(site.name, site.lon, site.lat))

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
<a href="http://geodesy.unr.edu/NGLStationPages/stations/{0}.sta">
    {0}</a>, {1:.3f} km from the epicenter of 2011 Tohoku earthquake.
<br>
<img src="http://geodesy.unr.edu/tsplots/IGS08/TimeSeries/{0}.png">
]]>'''.format(site.name, site.epi_dist)
    return description

def get_kml_html_description_for_seafloor(site):
    description = '''<![CDATA[
Seafloor station:  {0} <br>
{1:.3f} km from the epicenter of 2011 Tohoku earthquake. <br>
]]>'''.format(site.name, site.epi_dist)
    return description


def get_kml_html_description(site):
    if site.if_onshore:
        description = get_kml_html_description_for_onshore(site)
    elif site.if_seafloor:
        description = get_kml_html_description_for_seafloor(site)
    else:
        raise NotImplementedError()
    return description
