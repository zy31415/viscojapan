import os

from numpy import loadtxt, asarray
import numpy as np

from ..utils import _find_section, assert_strictly_assending_order,\
     assert_strictly_descending_order

__all__ = ['EarthModelFileReader']

class EarthModelFileReader(object):
    def __init__(self, earth_file):
        super().__init__()
        self.earth_file = earth_file
        assert os.path.exists(self.earth_file)

        self.RAD_EARTH = 6371.0
        self._rad_top = []
        self._rad_bot = []
        self._dep_top = []
        self._dep_bot = []
        self._density = []
        self._bulk = []
        self._shear = []
        self._shear_long = []
        self._visM = []
        self._visK = []
        
        self._parse_earth_file()
        self._check_order()

    def _parse_earth_file(self):
        with open(self.earth_file,'r') as fid:
            # skip the first line
            fid.readline()
            for ln in fid:
                self._parse_a_line(ln)

    def _parse_a_line(self, ln):
        br = ln.split()
        if len(br) == 6:
            rad_top, rad_bot, dep_top, rad_top, \
                     dep_bot, density, bulk, shear, \
                     shear_long, visK, visM = \
                     self._parse_6_items_line(br)                    
        elif len(br) == 8:
            rad_top, rad_bot, dep_top, rad_top, \
                     dep_bot, density, bulk, shear, \
                     shear_long, visK, visM = \
                     self._parse_8_items_line(br)
        else:
            raise ValueError('Earth file wrong.')

        self._rad_top.insert(0,rad_top) # km
        self._rad_bot.insert(0,rad_bot) # km 
        self._dep_top.insert(0,dep_top) # km
        self._dep_bot.insert(0,dep_bot) # km
        self._density.insert(0,density) # g/cm^3
        self._bulk.insert(0,bulk * 10**10) # Pa
        self._shear.insert(0,shear * 10**10) # Pa
        self._shear_long.insert(0,shear_long * 10**10) # Pa
        self._visK.insert(0,visK * 10**17) # Pa.s
        self._visM.insert(0,visM * 10**17) # Pa.s
        
        

    def _parse_6_items_line(self, broken_line):
        rad_top = float(broken_line[0])
        rad_bot = float(broken_line[1])
        dep_top = self.RAD_EARTH - rad_top
        dep_bot = self.RAD_EARTH - rad_bot
        density = float(broken_line[2])
        bulk = float(broken_line[3])
        shear = float(broken_line[4])
        shear_long = np.nan
        visK = np.nan     
        visM = float(broken_line[5])

        return rad_top, rad_bot, dep_top, rad_top, \
                     dep_bot, density, bulk, shear, \
                     shear_long, visK, visM
    
    def _parse_8_items_line(self, broken_line):
        rad_top = float(broken_line[0])
        rad_bot = float(broken_line[1])
        dep_top = self.RAD_EARTH - rad_top
        dep_bot = self.RAD_EARTH - rad_bot
        density = float(broken_line[2])
        bulk = float(broken_line[3])
        shear = float(broken_line[4])
        shear_long = float(broken_line[5])

        bl6 = broken_line[6]
        if bl6 == 'KKKKKKKKKKKK':
            visK = np.nan
        else:
            visK = float(bl6)

        bl7 = broken_line[7] 
        if bl7 == 'MMMMMMMMMMMM':
            visM = np.nan
        else:
            visM = float(bl7)

        return rad_top, rad_bot, dep_top, rad_top, \
                     dep_bot, density, bulk, shear, \
                     shear_long, visK, visM

    def _check_order(self):
        assert_strictly_assending_order(self.dep_top)
        assert_strictly_assending_order(self.dep_bot)
        assert_strictly_descending_order(self.rad_top)
        assert_strictly_descending_order(self.rad_bot)

    @property
    def dep_top(self):
        return np.asarray(self._dep_top)

    @property
    def dep_bot(self):
        return np.asarray(self._dep_bot)

    @property
    def rad_top(self):
        return np.asarray(self._rad_top)

    @property
    def rad_bot(self):
        return np.asarray(self._rad_bot)

    @property
    def density(self):
        return np.asarray(self._density, float)

    @property
    def shear(self):
        return np.asarray(self._shear, float)

    @property
    def bulk(self):
        return np.asarray(self._bulk, float)

    @property
    def shear_long(self):
        return np.asarray(self._shear_long, float)

    @property
    def visM(self):
        return np.asarray(self._visM,float)

    @property
    def visK(self):
        return np.asarray(self._visK,float)
    

    def _get_visM_by_dep_scalar(self, dep):
        nth = _find_section(self.dep_top, dep)
        return self.visM[nth]
    
    def get_visM_by_dep(self, dep):
        dep = np.asarray(dep)
        return np.vectorize(self._get_visM_by_dep_scalar)(dep)

    def _get_shear_by_dep_scalar(self, dep):
        nth = _find_section(self.dep_top, dep)
        return self.shear[nth]

    def get_shear_by_dep(self, dep):
        dep = np.asarray(dep)
        return np.vectorize(self._get_shear_by_dep_scalar)(dep)
        

    
