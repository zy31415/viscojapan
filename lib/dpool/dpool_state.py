from multiprocessing import Queue, Lock, Manager

class DPoolState(object):
    def __init__(self, tasks):
        self.lock_q_waiting = Lock()

        self.num_total_task = len(tasks)
        self.q_waiting = Queue()
        self._init_q_waiting(tasks)
            

        self.lock_q_aborted = Lock()
        self.q_aborted = Queue()

        self.lock_q_finished = Lock()
        self.q_finished = Queue()

        self.lock_running_tasks = Lock()
        manager = Manager()
        self.running_tasks = manager.list()

    def _init_q_waiting(self, tasks):
        for task in tasks:
            self.q_waiting.put(task)
            
    def if_has_more_task(self):
        res = (self.q_aborted.empty() and self.q_waiting.empty())
        return not res

    def pop_task(self):
        self.lock_q_aborted.acquire()
        self.lock_q_waiting.acquire()

        if not self.q_aborted.empty():
            task = self.q_aborted.get()
        else:
            task = self.q_waiting.get()

        self.lock_q_aborted.release()
        self.lock_q_waiting.release()
        return task

    # about running_tasks
    def register_running_tasks(self, pid):
        with self.lock_running_tasks:
            self.running_tasks.append((pid,None))

    def unregister_running_tasks(self, pid):
        with self.lock_running_tasks:
            nth = None
            for ni, ii in enumerate(self.running_tasks):
                if ii[0] == pid:
                    nth = ni
                    break
            del self.running_tasks[nth]

    def pop_running_tasks(self):
        with self.lock_running_tasks:
            res = self.running_tasks.pop()
        return res
            
    def update_running_tasks(self, pid, task):
        with self.lock_running_tasks:                
            nth = None
            for ni, ii in enumerate(self.running_tasks):
                if ii[0] == pid:
                    nth = ni
                    break
            del self.running_tasks[nth]
            self.running_tasks.append((pid, task))

    # about q_aborted:
    def register_aborted_task(self, task):
        with self.lock_q_aborted:
            self.q_aborted.put(task)
            
    # about q_finished
    def register_finished_task(self, task):
        with self.lock_q_finished:
            self.q_finished.put(task)

    
    def num_running_tasks(self):
        with self.lock_running_tasks:
            res = len(self.running_tasks)
        return res

    def num_waiting_tasks(self):
        self.lock_q_waiting.acquire()
        n2 = self.q_waiting.qsize()        
        self.lock_q_waiting.release()
        return n2

    def num_aborted_tasks(self):
        self.lock_q_aborted.acquire()
        n1 = self.q_aborted.qsize()
        self.lock_q_aborted.release()
        return n1
    
    def num_unfinished_tasks(self):
        self.lock_q_aborted.acquire()
        self.lock_q_waiting.acquire()

        n1 = self.q_aborted.qsize()
        n2 = self.q_waiting.qsize()
        
        self.lock_q_aborted.release()
        self.lock_q_waiting.release()

        return n1 + n2

    def print_unfinished_tasks(self):
        list(self.q_aborted[0])

    def get_all_running_pids(self):
        pids = []
        with self.lock_running_tasks:
            for pid in self.running_tasks:
                pids.append(pid)
        return pids

    def get_finished_tasks_list(self):
        tasks = []
        with self.lock_q_finished:
            while not self.q_finished.empty():
                tasks.append(self.q_finished.get(block=False))
        return tasks

    def __str__(self):
        ''' Output to sumarize pool state.
'''
        out = "Pool summary:\n"
        out += "    # unfinished tasks : %d\n"%self.num_unfinished_tasks()
        out += "    # waiting tasks : %d\n"%self.num_waiting_tasks()
        out += "    # aborted tasks : %d\n"%self.num_aborted_tasks()
        out += "    # running processes: %d"%self.num_running_tasks()
        return out
        
                
    
