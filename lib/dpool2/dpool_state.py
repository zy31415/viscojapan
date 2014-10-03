from multiprocessing import Queue, Lock, Manager
from queue import Empty

import numpy as np
import psutil as ps

from .utils import free_cpu

class DPoolState(object):
    def __init__(self, controller):

        self.SIZE_q_waiting = 200
        self.q_waiting = Queue(self.SIZE_q_waiting)
        self.q_running = Queue()
        self.q_finished = Queue()
        self.controller = controller
        
    def get_task(self):
        free_cpu_num = free_cpu()
        task = None
        if free_cpu_num > self.controller.threshold_kill:
            task = self.q_waiting.get()
        return task

    def add_running_task(self, pid, task):
        self.q_running.put((pid, task))

    # about q_finished
    def add_finished_task(self, task):
        self.q_finished.put(task)

    def num_waiting_tasks(self):
        n2 = self.q_waiting.qsize()        
        return n2

    def num_inline_tasks(self):
        return self.q_waiting.qsize()

    def get_all_running_tasks(self):
        pid_task = []
        while True:
            try:
                pid_task.append(self.q_running.get(block=False))
            except Empty:
                break
        return pid_task

    def get_all_finished_tasks(self):
        tasks = []
        while True:
            try:
                tasks.append(self.q_finished.get(block=False))
            except Empty:
                break
        return tasks

    def __str__(self):
        ''' Output to sumarize pool state.
'''
        out = "Pool summary:\n"
        out += "    # waiting tasks : %d\n"%self.num_waiting_tasks()
        return out
        
                
    
