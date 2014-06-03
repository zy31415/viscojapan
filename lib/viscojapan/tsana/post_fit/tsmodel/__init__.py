__doc__ = """This package do the computing and modeling using original data."""

__submodules__ = ['data','errors','funcs',
                  'reg_models','reg_routines_lin','reg_routines_ml','plot']
 
# import submodules:
from .data import *
from .errors import *
from .funcs import *
from .reg_models import *
from .reg_routines_lin import *
from .reg_routines_ml import *
from .plot import *

# define all functions:
__all__ = []
for mod in __submodules__:
    __all__ += globals()[mod].__all__
