import subprocess, signal
from subprocess import call
import os
import datetime

import psutil as ps

from .controller import Controller
from .dpool_state import DPoolState
from .dpool_process import DPoolProcess
from .task import Task
from .feeder import Feeder

def mean(arr):
    return sum(arr)/len(arr)

def free_cpu(interval=0.1):
    cpu_percent = ps.cpu_percent(interval=interval)
    ncpu = ps.cpu_count()
    return ncpu * (1. - cpu_percent/100.)

def print_free_cpu():
    print('Free CPU #:')
    print('    %.2f'%free_cpu())

def find_process_by_pid(processes, pid):
    for p in processes:
        if p.pid == pid:
            return p
    raise ValueError('PID %d is not found.'%pid)


def kill_child_processes(parent_pid, sig=signal.SIGTERM):
        ps_command = subprocess.Popen('pstree -p %d | perl -ne \'print "$1 " while /\((\d+)\)/g\'' %\
                                      parent_pid,
                                      shell=True, stdout=subprocess.PIPE)
        ps_output = ps_command.stdout.read().decode()
        retcode = ps_command.wait()
        assert retcode == 0, "ps command returned %d" % retcode
        for pid_str in ps_output.split():
            try:
                os.kill(int(pid_str), sig)
            except ProcessLookupError as err:
                print('    ',str(err))                


def remove_process_by_pids(processes, pids):
    for pid in pids:
        p = find_process_by_pid(pid)
        processes.remove(p)

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
        print('    PID %d is started.'%p.pid)
        self.running_procs.append(p)

    def _add_procs(self, n):
        n = int(n)
        n_left = self.dp_state.num_inline_tasks()
        n = min(n, n_left)        
        if n > 0:
            print('    %d processes will be added.'%n)
            for ii in range(n):
                self._add_a_process()

    def update_running_task(self):
        pid_tasks = self.dp_state.get_all_running_tasks()
        pids_to_remove = []
        for pid, task in pid_tasks:
            p = find_process_by_pid(self.running_procs, pid)
            if (task == 'Done'):
                pids_to_remove.append(pid)
            p.task = task

        remove_process_by_pids(
            self.running_procs, pids_to_remove)

    def _kill_a_process(self):
        if len(self.running_procs) > 0:
            while not hasattr(self.running_procs[-1], 'task'):
                print(' Updating running task...')
                self.update_running_task()
            p = self.running_procs.pop()
            print("    Termination: PID: %d, Task: %s"%\
                  (p.pid, str(p.task)))
            kill_child_processes(p.pid)
            self.dp_state.add_aborted_task(p.task)

    def _kill_procs(self, n):
        n = int(n)
        if n>0:
            print('    %d processes will be deleted.'%n)
            for ii in range(n):
                self._kill_a_process()

    def _dynamic_pool_adjust_process(self):
        self._add_procs(free_cpu() - self.controller.threshold_load)
        self._kill_procs(self.controller.threshold_kill - free_cpu())

    def _static_pool_adjust_process(self):
        self._add_procs(self.controller.num_processes -
                        self.num_running_tasks)
        
        self._kill_procs(self.num_running_tasks -
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
        print("Execution summary:")
        print('    # total tasks : %d'%self.num_total_tasks)
        print('    # unhandled tasks : %d'%self.num_unhandled_tasks)
        print("    # running processes: %d"%self.num_running_tasks)
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
        if self.num_running_tasks > 0:
            t /= self.num_running_tasks
        return t

    def _compute_time_needed_to_finish(self):
        t = self._compute_average_exe_time() * \
            self.num_unfinished_tasks
        if self.num_running_tasks > 0:
            t /= self.num_running_tasks
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
    def num_running_tasks(self):
        return len(self.running_procs)

    @property
    def num_unhandled_tasks(self):
        return len(self.tasks)

    @property
    def num_unfinished_tasks(self):
        return self.num_total_tasks - self.num_finished_tasks
            
    def run(self):
        feeder = Feeder(self.tasks, self.dp_state)
        feeder.start()
        
        while self.num_finished_tasks < self.num_total_tasks:
            self.cls()
            self.controller.update()
            self.update_running_task()
            if self.controller.if_fix == 0:
                self._dynamic_pool_adjust_process()
            elif self.controller.if_fix == 1:
                self._static_pool_adjust_process()

        feeder.join()
        self._join_all_procs()

        print('Done.')
        

    

    
