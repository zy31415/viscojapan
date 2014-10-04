import subprocess, signal
from subprocess import call
import os
import datetime
import time
from numpy import loadtxt, mean

import psutil as ps

from .controller import Controller
from .dpool_state import DPoolState
from .dpool_process import DPoolProcess
from .task import Task
from .feeder import Feeder
from .utils import free_cpu

def print_free_cpu():
    print('Free CPU #:')
    print('    %.2f'%free_cpu())

def find_process_by_pid(processes, pid):
    for p in processes:
        if p.pid == pid:
            return p
    raise ValueError('PID %d is not found.'%pid)

def remove_process_by_pids(processes, pids):
    for pid in pids:
        p = find_process_by_pid(processes, pid)
        processes.remove(p)

class DPool(object):
    def __init__(self,
                 tasks,
                 controller_file = 'pool.config',):

        self.tasks = tasks
        self.num_total_tasks = len(tasks)        
        self.controller = Controller(controller_file)
        self.dp_state = DPoolState(self.controller)
        self._finished_tasks = []
        self.processes = []
    
    def _add_a_process(self):
        p = DPoolProcess(dp_state=self.dp_state)
        p.start()
        print('    PID %d is started.'%p.pid)
        self.processes.append(p)

    def _add_procs(self, n):
        n = int(n)
        n_left = self.dp_state.num_waiting_tasks()
        n = min(n, n_left)        
        if n > 0:
            print('    %d processes will be added.'%n)
            for ii in range(n):
                self._add_a_process()
            time.sleep(1)


    def _dynamic_pool_adjust_process(self):
        self._add_procs(free_cpu() - self.controller.threshold_load)

    def _static_pool_adjust_process(self):
        self._add_procs(self.controller.num_processes -
                        self.num_running_tasks)        

    def _join_all_procs(self):
        for p in self.running_procs:
            p.join()
            
    def cls(self):
        call('clear',shell=True)
        print(self.controller)
        print_free_cpu()
        print(self.dp_state)
        self.print_exe_summary()
        self.print_finished_tasks()

    def print_finished_tasks(self, n=6):
        ll = self.finished_tasks
        N = self.num_finished_tasks
        print('Finished tasks summarize:')
        print('    ......')
        for nth in range(min(N,n),1,-1):
            print(ll[-nth])

    def print_exe_summary(self):
        print("Execution summary:")
        print('    # total tasks : %d'%self.num_total_tasks)
        print('    # unhandled tasks : %d'%self.num_unhandled_tasks)
        print("    # processes: %d"%self.num_processes)
        print('    average exe time: %.2f sec'%\
              self._compute_average_exe_time())
        print('    Est. total exe time: %.2f hr'%\
              (self._compute_total_exe_time()/3600.))
        print('    Est. finishing at: %s'%\
              self._compute_finishing_time().strftime("%A %d. %B %Y %H:%M" ))
        
    def _compute_average_exe_time(self):
        ts = []
        for task in self.finished_tasks:
            if task.t_consumed < 0.1:
                continue
            ts.append(task.t_consumed)
        if len(ts) == 0:
            return 0.
        return mean(ts)

    def _compute_total_exe_time(self):        
        t = self._compute_average_exe_time() * \
            self.num_total_tasks
        if self.num_processes > 0:
            t /= self.num_processes
        return t

    def _compute_time_needed_to_finish(self):
        t = self._compute_average_exe_time() * \
            self.num_unfinished_tasks
        if self.num_processes > 0:
            t /= self.num_processes
        return t

    def _compute_finishing_time(self):
        dt = self._compute_time_needed_to_finish()
        now = datetime.datetime.now()
        ft = now + datetime.timedelta(seconds = dt)
        return ft

    @property
    def finished_tasks(self):
        self._finished_tasks += self.dp_state.get_all_finished_tasks()
        return self._finished_tasks

    @property
    def num_finished_tasks(self):
        return len(self.finished_tasks)

    @property
    def num_unhandled_tasks(self):
        return len(self.tasks)

    @property
    def num_unfinished_tasks(self):
        return self.num_total_tasks - self.num_finished_tasks

    @property
    def num_processes(self):
        return self.dp_state.num_processes.value
            
    def run(self):
        print('Loading tasks ...')
        for task in self.tasks:
            self.dp_state.q_waiting.put(task)            
                
        while self.dp_state.num_waiting_tasks() > 0:
            self.cls()
            self.controller.update_and_sleep()
            if self.controller.if_fix == 0:
                self._dynamic_pool_adjust_process()
            elif self.controller.if_fix == 1:
                self._static_pool_adjust_process()
        
        for p in self.processes:
            p.join()

        print('Done.')
        

    

    
