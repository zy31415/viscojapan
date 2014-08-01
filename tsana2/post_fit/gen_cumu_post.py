import pickle
from multiprocessing import Pool, Lock, Process

from h5py import File
from numpy import loadtxt, asarray, savetxt, zeros

import viscojapan as vj
from viscojapan.tsana import get_cumu_post

sites = loadtxt('sites/sites','4a')

def get_cumu_disp(sites,day):
    res=zeros((len(sites),3))
    
    for nth, site in enumerate(sites):
        with open('CFS_POST/%s-res.cfs'%site.decode(), 'rb') as fid:
            cfs = pickle.load(fid)
        res[nth,:]=get_cumu_post(cfs, day)
    
    return asarray(res, float)

fep = vj.EpochalData('cumu_post_predicted.h5')
fep['sites'] = sites

def func(day):
    print(day)
    disp = get_cumu_disp(func.sites, day)
    with func.lock:
        func.fep[day] = disp

def init(func, sites, fep, lock):
    func.sites = sites
    func.fep = fep
    func.lock = lock

if __name__ == '__main__':
    lock = Lock()
    days = range(0,1200)
    pool = Pool(processes = 5, initializer = init, initargs=(func, sites, fep, lock))
    pool.map(func, days)
