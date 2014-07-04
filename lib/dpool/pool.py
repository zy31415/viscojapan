#!/usr/bin/env python3
''' Use a dynamic pool to run a multiprocess task.
Number of works is decided by availibility of CPUs.
'''
from numpy import ceil
from os.path import join, exists
from os import makedirs
import os
from shutil import move
from time import sleep
from subprocess import call,check_output,CalledProcessError
from multiprocessing import Process, cpu_count

__all__=['Pool']

def ncpus(wait=0):
    ''' Number of available cpus on the system.
'''
    sleep(wait)
    tp=check_output('top -b -n 3 | grep "Cpu(s)" | tail -n 1',shell=True).decode()
    print('   %s'%tp)
    tp=tp.split(':')[1]
    tp=tp.split(',')
    us=float(tp[0].split('%')[0])/100.
    idle=float(tp[3].split('%')[0])/100.
    ncpu=cpu_count()
    return ncpu*idle


def log_err_terminate(par,msg=''):
    d='err_terminate/'
    if not exists(d):
        makedirs(d)
    with open(join(d,'err_term_%s'%par),'w') as fid:
        fid.write(msg)

## @class Pool
# @brief Pool of processes.
# @section task_and_workers tasks and workers
# - tasks - works need to be done
# - workers - works that are doing
#
# @section controller controller file
#
# controller = 'dyn_pool.config'
# 
# The file is used to control pool of workers.
#
# File format:
#
# This config file is used to control the dynamic pool.
# - 1st column,if_fix, 0-False, dynamic pool; 1-True, static pool
#
# if if_fix == 0 (False)
# - 2st column, load, threashold of number of cpus left to load a task
# - 3nd column, kill, threashold of number of cpus left to kill tasks
# - 4rd column, sleep, sleep time for the next check in sec.
#
# if if_fix == 1 (True)
# - 2st column, number of processes
# - 3nd column, Not used,
# - 4rd column, sleep, sleep time for the next check in sec.
#
class Pool:
    def __init__(self):
        # Two fundamental list, tasks and workers:
        self.tasks=None
        
        # Class or function used to generate workers
        self._workers=[]

        self.nload=20 # number of initial loading        

        # Parameters used to control the pool:
        self._sleep=5
        self.controller='pool.config'
        self._if_fix=None
        self._load=None
        self._kill=None        
        self._nproc=None

    def clean_workers(self):
        ''' Remove dead workers from the workers list.
    '''
        out=[]
        for w in self._workers:
            if not w.is_alive():
                out.append(w)
        for w in out:
            self._workers.remove(w)

    def get_workers(self):
        '''
'''
        self.clean_workers()
        return self._workers

    def add_worker(self,p):
        '''
'''
        self._workers.append(p)
        

    def update_controller(self):
        ''' File used to control the pool:
# - comment line
1st coloum: threashold of number of cpus to load a task
2nd coloum: threashold of number of cpus to kill tasks
3rd coloum: sleep time for the next check in sec.
'''
        with open(self.controller) as fid:
            for ln in fid:
                if ln.strip()[0]!='#':
                    break                
            tp=ln.strip().split()
        if_fix=bool(int(tp[0]))
        self._if_fix=if_fix
        if not if_fix:
            load=float(tp[1])
            kill=float(tp[2])
            if load <=kill:
                raise ValueError('load(=%d) should larger than kill(=%d)!'%(load, kill))    
            sleep=int(tp[3])
            self._load=load
            self._kill=kill
            self._sleep=sleep
        else:
            nprocess=int(tp[1])
            sleep=int(tp[3])
            self._nproc=nprocess
            self._sleep=sleep

    def sleep(self):
        ''' Sleep the program.
'''
        sleep(self._sleep) 

    def init_load(self):
        ''' Initial load of the system.
'''
        print('Initial loading ...')
        for n in range(0,self.nload):
            task=self.pop_task()
            task.start()
            self.add_worker(task)
        
    def pop_task(self,verbose=True):
        ''' Get an unfinished task.
'''
        task=self.tasks.pop()
        while task.if_output_exist():
            if verbose:
                print('  %s Results found! Skipped!'%task)
            task.log_succ()
            task=self.tasks.pop()
        return task
    
    def load_tasks(self,n):
        ''' Load n number of tasks.
'''
        for ni in range(0,n):
            task=self.pop_task()
            task.start()
            print('    %s (PID=%d)is loaded.'%(task.name,task.pid))
            self.add_worker(task)
        
    def kill_tasks(self,n):
        ''' Kill n number of tasks.
'''
        for ni in range(0,n):
            workers=self.get_workers()
            if workers:                        
                w=workers[-1]
                try:
                    w.terminate() # terminate one unfinished process
                    print('    Process %s (PID %d) is killed'%(w.name,w.pid))
                except CalledProcessError as err:
                    print('  '+str(err))
                    log_err_terminate(w.name,str(err))
                self.tasks.append(w.copy()) # add back to tasks list
                workers.pop() # pop out from running process list                
            else:
                print('    No process to kill. Program is holding!')

    def adjust_tasks(self,n):
        '''
'''
        m=int(n)
        if n>0:
            print('    %f (%d) processes will be loaded.'%(n,m))
            self.load_tasks(m)
        elif n<0:
            print('    %f (%d) processes will be killed.'%(-n,-m))
            self.kill_tasks(-m)
        else:
            print('    Nothing happened.')

    def analyze_controller(self):
        if self._if_fix:
            nworkers=len(self.get_workers())
            return self._nproc - nworkers

        if ncpus()>self._load: # load
            n=ncpus()-self._load
            n=min(n,len(self.tasks)) # make sure not loading more than need
            return n

        if ncpus()<self._kill: # kill
            n= ncpus()-self._load
            return n
        return 0
    
    def cls(self):
        call('clear',shell=True)
        print("Number of unfinished tasks:%d"%len(self.tasks))
        print(['...']+[ii.name for ii in self.tasks[-20:]])
        print('')
        print("Number of running workers:%d"%len(self.get_workers()))
        print([ii.name for ii in self.get_workers()])
        if self._if_fix!=None:
            print('')
            print('Pool config (%s):'%self.controller)
            if self._if_fix:
                print('    Static: nproc = %f, sleep = %d\n'%(self._nproc,self._sleep))
            else:
                print('    Dynamic: load = %f, kill = %f, sleep = %d\n'%(self._load,self._kill,self._sleep))
            
    def start(self):
        # Initial load of the system:
        try:
            self.init_load()
            self.sleep()
            self.cls()
            
            while self.tasks:
                self.update_controller()
                n=self.analyze_controller()
                self.adjust_tasks(n)
                self.sleep()
                self.cls()
        except IndexError as err:
            print('Job done!')
           
if __name__=='__main__':
    pass    
        
    
    
