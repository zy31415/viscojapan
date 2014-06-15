import os
from os.path import join

from numpy import ones, loadtxt, arange

from viscojapan.epochal_data.epochal_data import EpochalData

def delete_if_exists(fn):
    if os.path.exists(fn):
        os.remove(fn)

_dir_data = os.path.dirname(os.path.abspath(__file__))


def read_sites_file():
    sites = loadtxt(join(_dir_data,'sites'),'4a,')
    return sites

def set_epoch_value(fn):
    epochs = range(1, 10)
    ep = EpochalData(fn)
    sites = read_sites_file()
    for epoch in epochs:
        nrows = len(sites)*3
        val = arange(nrows).reshape([-1,1])
        ep.set_epoch_value(epoch, val)

def set_sites_info(fn):
    ep = EpochalData(fn)
    ep.set_info('sites',read_sites_file())

def create_a_sites_data_file(fn):
    delete_if_exists(fn)
    set_epoch_value(fn)
    set_sites_info(fn)
    
