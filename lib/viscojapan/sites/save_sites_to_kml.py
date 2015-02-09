import simplekml as sk

from ..sites_db import get_site_true_name

__author__ = 'zy'
__all__=['save_sites_to_kml']

def save_sites_to_kml(sites, fn, label_color='red', icon_name='flag'):
    kml = sk.Kml()
    for site in sites:
        site_id= site.id
        site_name = get_site_true_name(site)

        pnt = kml.newpoint(name = site_name)
        pnt.coords = [(site.lon, site.lat)]
        pnt.style.labelstyle.color = get_kml_color(label_color)
        pnt.style.iconstyle.icon.href = get_kml_icon_link(icon_name)
        pnt.description = get_kml_html_description(site)
    kml.save(fn)

def get_kml_color(label_color):
    if label_color == 'red':
        out = sk.Color.red
    else:
        raise NotImplementedError('Not recognized color.')
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
        raise NotImplementedError('Not recognized icon name.')
    return out

def get_kml_html_description_for_onshore(site):
    description = '''<![CDATA[
<a href="http://geodesy.unr.edu/NGLStationPages/stations/{id}.sta">
    {name} ({id})</a>
<br>
<img src="http://geodesy.unr.edu/tsplots/IGS08/TimeSeries/{id}.png">
]]>'''.format(id=site.id, name=get_site_true_name(site))
    return description

def get_kml_html_description_for_seafloor(site):
    description = '''<![CDATA[
Seafloor station:  {name}{id} <br>
<br>
]]>'''.format(id=site.id, name=get_site_true_name(site))
    return description


def get_kml_html_description(site):
    if site.if_onshore:
        description = get_kml_html_description_for_onshore(site)
    elif site.if_seafloor:
        description = get_kml_html_description_for_seafloor(site)
    else:
        raise NotImplementedError()
    return description

