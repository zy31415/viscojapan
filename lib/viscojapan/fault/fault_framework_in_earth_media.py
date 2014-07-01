from os.path import join

from numpy import loadtxt, vectorize, asarray

from .fault_framework import FaultFramework
from .utils import _find_section, my_vectorize
from ..utils import get_this_script_dir

this_file_path = get_this_script_dir(__file__)

_earth_file= join(this_file_path, 'earth.model')


class FaultFrameworkInEarthMedia(FaultFramework):
    def __init__(self, earth_file=_earth_file):
        super().__init__()
        self.earth_file = earth_file
        self._read_earth_file()

    def _read_earth_file(self):
        tp=loadtxt(self.earth_file, skiprows=1)
        dep0 = (6371. - tp[:,0])[-1::-1]
        dep1 = (6371. - tp[:,1])[-1::-1]
        self.DEP_SHEAR = dep0
        self.SHEAR_MODULUS=(tp[:,4]*1e10)[-1::-1] # Pa

    def _get_shear_scalar(self, dep):
        print(dep)
        nth = _find_section(self.DEP_SHEAR, dep)
        return self.SHEAR_MODULUS[nth]

    def get_shear(self,dep):
        return my_vectorize(self._get_shear_scalar, dep)

