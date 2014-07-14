from multiprocessing import Queue, Lock, Manager
from queue import Empty

class DPoolState(object):
    def __init__(self ):
        self.lock_q_waiting = Lock()

        self.q_waiting = Queue()
        
        self.lock_q_aborted = Lock()
        self.q_aborted = Queue()

        self.lock_q_finished = Lock()
        self.q_finished = Queue()

        self.lock_running_tasks = Lock()
        manager = Manager()
        self.running_tasks = manager.list()

    def add_tasks(self, tasks):
        for task in tasks:
            self.q_waiting.put(task)
            
##    def if_has_more_task(self):
##        res = (self.q_aborted.empty() and self.q_waiting.empty())
##        return not res

    def pop_task(self):
        try:
            task = self.q_aborted.get(block=False)
        except Empty:
            print("    No task availabel in abroted list.")
            try:
                task = self.q_waiting.get(timeout = 10.)
            except Empty:
                print('    No task availabel in waiting list.')
                task = None
        return task

    def _find_running_task_by_pid(self,pid):
        nth = None
        for ni, ii in enumerate(self.running_tasks):
            if ii[0] == pid:
                nth = ni
                break
        if nth is None:
            #raise ValueError("   PID %d is not found."%pid)
            print("   PID %d is not found."%pid)
            return None
        return nth

    def _delete_from_running_tasks_by_pid(self,pid):
        nth = self._find_running_task_by_pid(pid)
        if nth is not None:
            del self.running_tasks[nth]

    # about running_tasks
    def register_running_tasks(self, pid):
        with self.lock_running_tasks:
            self.running_tasks.append((pid,None))

    def unregister_running_tasks(self, pid):
        with self.lock_running_tasks:
            self._delete_from_running_tasks_by_pid(pid)

    def pop_running_tasks(self):
        try:
            res = self.running_tasks.pop()
        except Exception as exp:
            print(exp)
            res = (None, None)
        return res
    
    def update_running_tasks(self, pid, task):
        with self.lock_running_tasks:                
            self._delete_from_running_tasks_by_pid(pid)
            self.running_tasks.append((pid, task))

    # about q_aborted:
    def register_aborted_task(self, task):
        self.q_aborted.put(task)
            
    # about q_finished
    def register_finished_task(self, task):
        self.q_finished.put(task)

    
    def num_running_tasks(self):
        res = len(self.running_tasks)
        return res

    def num_waiting_tasks(self):
        self.lock_q_waiting.acquire()
        n2 = self.q_waiting.qsize()        
        self.lock_q_waiting.release()
        return n2

    def num_aborted_tasks(self):
        n1 = self.q_aborted.qsize()
        return n1
    
    def num_unfinished_tasks(self):
        n1 = self.q_aborted.qsize()
        n2 = self.q_waiting.qsize()
        return n1 + n2

    def get_all_running_pids(self):
        pids = []
        with self.lock_running_tasks:
            for pid in self.running_tasks:
                pids.append(pid)
        return pids

    def get_finished_tasks_list(self):
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
        out += "    # aborted tasks : %d\n"%self.num_aborted_tasks()
        out += "    # running processes: %d"%self.num_running_tasks()
        return out
        
                
    
