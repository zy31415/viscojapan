import numpy as np

__author__ = 'zy'

__all__ = ['mo_to_mw','mw_to_mo']

def mo_to_mw(mo):
    return 2./3.*np.log10(mo) - 6.

def mw_to_mo(mw):
    return 10**((3.*mw+18.)/2.)
