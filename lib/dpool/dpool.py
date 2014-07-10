from subprocess import call
import os
import datetime

import psutil as ps

from .controller import Controller
from .dpool_state import DPoolState
from .dpool_process import DPoolProcess
from .task import Task

def mean(arr):
    return sum(arr)/len(arr)

def free_cpu(interval=0.1):
    cpu_percent = ps.cpu_percent(interval=interval)
    ncpu = ps.cpu_count()
    return ncpu * (1. - cpu_percent/100.)

def print_free_cpu():
    print('Free CPU #:')
    print('    %.2f'%free_cpu())

class DPool(object):
    def __init__(self,
                 tasks,
                 controller_file = 'pool.config',):

        self.tasks = tasks
        self.num_total_tasks = len(tasks)
        self.dp_state = DPoolState()
        self.controller = Controller(controller_file)
        self._finished_tasks = []
        self.running_procs = []
    
    def _add_a_process(self):
        p = DPoolProcess(dp_state=self.dp_state)
        p.start()
        self.running_procs.append(p)

    def _add_procs(self, n):
        n = int(n)
        n_left = self.dp_state.num_unfinished_tasks()
        n = min(n, n_left)
        if n > 0:
            print('    #%d running processes will be added.'%n)
            for ii in range(n):
                self._add_a_process()

    def _kill_a_process(self):
        pid, task = self.dp_state.pop_running_tasks()
        if task is not None:
            self.dp_state.register_aborted_task(task)
        if pid is not None:
            self._send_terminate_signal_to_process(pid)

    def _send_terminate_signal_to_process(self, pid):
        for p in self.running_procs:
            if p.pid == pid:
                p.terminate()
                return
        raise ValueError('Process is not found.')

    def _kill_procs(self, n):
        n = int(n)
        if n>0:
            print('    #%d running processes will be deleted.'%n)
            for ii in range(n):
                self._kill_a_process()

    def _dynamic_pool_adjust_process(self):
        self._add_procs(free_cpu() - self.controller.threshold_load)
        self._kill_procs(self.controller.threshold_kill - free_cpu())

    def _static_pool_adjust_process(self):
        self._add_procs(self.controller.num_processes -
                        self.dp_state.num_running_tasks())
        
        self._kill_procs(self.dp_state.num_running_tasks() -
                         self.controller.num_processes)

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
        print('    # total tasks : %d'%self.num_total_tasks)
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
        return t

    def _compute_time_needed_to_finish(self):
        t = self._compute_average_exe_time() * \
            self.dp_state.num_unfinished_tasks()
        return t

    def _compute_finishing_time(self):
        dt = self._compute_time_needed_to_finish()
        now = datetime.datetime.now()

        ft = now + datetime.timedelta(seconds = dt)

        return ft

    @property
    def finished_tasks(self):
        self._finished_tasks += self.dp_state.get_finished_tasks_list()
        return self._finished_tasks

    @property
    def num_finished_tasks(self):
        return len(self.finished_tasks)
            
    def run(self):
        self.dp_state.add_tasks(self.tasks)
        while self.num_finished_tasks < self.num_total_tasks:
            self.cls()
            self.controller.update()
            if self.controller.if_fix == 0:
                self._dynamic_pool_adjust_process()
            elif self.controller.if_fix == 1:
                self._static_pool_adjust_process()

        self._join_all_procs()

        print('Done.')
        
            
        


    

    
