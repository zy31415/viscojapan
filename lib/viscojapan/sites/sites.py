from os.path import join

import numpy as np
import pyproj as pj
import simplekml as sk

import viscojapan as vj

this_file_path = vj.get_this_script_dir(__file__)

__all__ = ['Site', 'Sites']

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
    
def read_sites_position_file(sites_file):
    tp = np.loadtxt(sites_file,'4a, 2f')
    return {ii[0].decode():ii[1] for ii in tp}


class SitePosDictSingleton(object):
    ''' Read from sites position file.
This is designed as a singleton to keep times of file reading action,
which is very slow, being minimum.
'''
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SitePosDictSingleton,
                                 cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.sites_pos_file = join(this_file_path, 'share/sites_with_seafloor')
        self._pos_dic = read_sites_position_file(self.sites_pos_file)

    def __getitem__(self, site):
        assert site in self._pos_dic
        return self._pos_dic[site]

    @property
    def names(self):
        return sorted([ii for ii in self._pos_dic.keys()])
        

class Site(object):
    ''' Represent a site.
'''
    _site_pos_dic = SitePosDictSingleton()    
    def __init__(self, name):
        assert isinstance(name, str), 'name type is str.'
        self._name = name
        self._load_lonlat()

    def _load_lonlat(self):
        tp = Site._site_pos_dic[self._name]
        self._lon = tp[0]
        self._lat = tp[1]
        
    @property
    def name(self) -> str:
        return self._name

    @property
    def lon(self) -> bool:
        return self._lon        

    @property
    def lat(self) -> bool:
        return self._lat

    @property
    def if_seafloor(self)  -> bool:
        if self._name[0] == '_':
            return True
        else:
            return False

    @property
    def if_onshore(self) -> bool:
        if self._name[0] == '_':
            return False
        else:
            return True

    @property
    def epi_dist(self) -> float:
        ''' Distance from the epicenter in KM.
'''
        epi_lon0, epi_lat0 = vj.TOHOKU_EPICENTER
        p = pj.Geod(ellps='WGS84')
        az1, az2, dis = p.inv(self.lon, self.lat, epi_lon0, epi_lat0)
        return dis/1000.

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        out = '%s at (%8.4f, %8.4f), %8.3f km from the epi.'%\
               (self.name, self.lon, self.lat, self.epi_dist)
        #out += '\n  %s\n'%(super().__str__())
        return out
        
class Sites(object):
    ''' Represent a sites list.
'''
    def __init__(self, sites):
        self._sites_list = []
        for site in sites:
            if isinstance(site, str):
                self._sites_list.append(Site(site))
            elif isinstance(site, Site):
                self._sites_list.append(site)
            else:
                raise ValueError('site should be either string or Site type.')

    @classmethod
    def init_including_all(cls) -> object:
        return cls(SitePosDictSingleton().names)

    @classmethod
    def init_from_txt(cls,fn):
        sites = np.loadtxt(fn, '4a', usecols=(0,))
        sites = [ii.decode() for ii in sites]
        return cls(sites)
        
    @property
    def names(self):
        return [ii.name for ii in self]

    @property
    def names_bytes(self):
        return [ii.name.encode() for ii in self]

    @property
    def names_seafloor(self):
        out = []
        for site in self:
            if site.if_seafloor:
                out.append(site.name)
        return out

    @property
    def names_onshore(self):
        out = []
        for site in self:
            if site.if_onshore:
                out.append(site.name)
        return out

    @property
    def ch_seafloor(self):
        return np.asarray([site.if_seafloor for site in self])

    @property
    def ch_onshore(self):
        return np.asarray([site.if_onshore for site in self])
        

    def save2txt(self, fn, header=None):
        with open(fn, 'wt') as fid:
            if header is not None:
                fid.write(header)
                if header[-1] != '\n':
                    fid.write('\n')                
            fid.write('# site lon lat\n')
            for site in self:
                fid.write('%s %f %f \n'%(site.name, site.lon, site.lat))   

    def save2kml(self, fn, label_color='red', icon_name='flag'):
        kml = sk.Kml()
        for site in self:
            pnt = kml.newpoint(name = site.name)
            pnt.coords = [(site.lon, site.lat)]
            pnt.style.labelstyle.color = get_kml_color(label_color)
            pnt.style.iconstyle.icon.href = get_kml_icon_link(icon_name)
            pnt.description = get_kml_html_description(site)
        kml.save(fn)

    @property
    def num_sites(self):
        return len(self.names)

    def __len__(self):
        return self.num_sites

    def __iter__(self):
        for site in self._sites_list:
            yield site
    
