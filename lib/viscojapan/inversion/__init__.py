from .deconvolution import Deconvolution
from .occam_deconvolution_separate_co_post import *
from .occam_deconvolution_separate_co_post2 import *
from .static_inversion import StaticInversion
from .occam_deconvolution import *
from .result_file import *
try:
    from .predict_displacement import *
except ImportError:
    print("    Cannot import sqlite3.")

from . import regularization as reg
from . import basis_function as basis

__author__ = 'zy'

