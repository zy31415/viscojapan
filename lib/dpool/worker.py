#!/usr/bin/env python3
''' Use a dynamic pool to run a multiprocess task.
Number of works is decided by availibility of CPUs.
'''
from numpy import ceil
from os.path import join, exists
from os import makedirs, kill
from shutil import move
from time import sleep
from subprocess import call,check_output,CalledProcessError
from multiprocessing import Process, cpu_count
import re, signal
from abc import ABCMeta, abstractmethod
from copy import deepcopy

__all__=['Worker']

def get_children_pid(pid):
    ''' Return all the children of a pid.
'''
    tp=check_output("pstree -p -n %d"%pid,shell=True)
    tp=tp.decode()
    out=re.findall('\([0-9]*\)',tp)
    cpids=[]
    for o in out:
        cpids.append(int(o[1:-1]))
    return cpids

def kill_child_processes(pid, sig=signal.SIGTERM):
    pids=get_children_pid(pid)
    print(pids)
    for p in pids:
        kill(p,sig)

def ncpus(wait=10):
    ''' Number of available cpus on the system.
'''
    sleep(wait)
    ocpu=check_output("ps aux | awk '{sum += $3} END {print sum}'",shell=True)
    ocpu=ceil(float(ocpu.decode())/100.)
    acpu=cpu_count()
    return int(acpu-ocpu)

def gen_output_file(par):
    tp=par.split('#')
    dep=int(tp[0][0:3])
    vis_no=int(tp[1][3:6])
    pday=int(tp[2][3:8])
    fno=int(tp[3])
    f_out='work/%03dkm-vis%02d/outs/outs_day%05d/out_%02d'%\
                  (dep,vis_no,pday,fno)
    return f_out


def log_err_terminate(par,msg=''):
    d='err_terminate/'
    if not exists(d):
        makedirs(d)
    with open(join(d,'err_term_%s'%par,'w')) as fid:
        fid.write(msg)

class Worker(Process,metaclass=ABCMeta):
    ''' Worker class used by class Pool.
This is an abstract class. You have to implement your own worker class.
'''
    @abstractmethod
    def if_output_exist(self):
        ''' Check if output exist.
'''
        pass
    
    @abstractmethod
    def run(self):
        ''' Process task is defined here.
'''
        pass

    def terminate(self):
        ''' Terminate the process.
'''
        kill_child_processes(self.pid)
        super().terminate()

    def __str__(self):
        ''' String represents the process.
'''
        return self.name

    def copy(self):
        ''' Abstract copy class.
'''
        return self.__class__(self.name)

    def log_succ(self,msg=''):
        ''' Log a successful run.
'''
        if not exists('succ/'):
            makedirs('succ/')
        with open('succ/%s'%(self.name),'w') as fid:
            fid.write(msg)

    def log_err(par,msg=''):
        ''' Log an error run.
'''
        if not exists('err/'):
            makedirs('err/')
        f='err/err_%s'%par
        with open(f,'w') as fid:
            fid.write(msg)

if __name__=='__main__':
    pass

    
