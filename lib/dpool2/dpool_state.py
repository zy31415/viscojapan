from multiprocessing import Queue, Lock, Manager, Value
from queue import Empty

import numpy as np
import psutil as ps

from .utils import free_cpu

class DPoolState(object):
    def __init__(self, controller):

        self.SIZE_q_waiting = 200
        self.q_waiting = Queue(self.SIZE_q_waiting)
        self.q_finished = Queue()
        self.controller = controller
        self.num_processes = Value('i',0)
        
    def get_task(self):
        free_cpu_num = free_cpu()
        task = None
        try:
            if free_cpu_num > self.controller.threshold_kill:
                if self.num_waiting_tasks() > 0:
                    task = self.q_waiting.get(timeout=self.controller.sleep_interval)
        except Empty:
            pass
        return task

    # about q_finished
    def add_finished_task(self, task):
        self.q_finished.put(task)

    def num_waiting_tasks(self):
        n2 = self.q_waiting.qsize()        
        return n2
    
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
        
                
    
