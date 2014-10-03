from multiprocessing import Process

class DPoolProcess(Process):
    def __init__(self, dp_state):
        super().__init__()
        self.dp_state = dp_state
        self.dp_state.num_processes.value += 1

   
    def run(self):
        state = self.dp_state
        task = state.get_task()
        while task is not None:
            task.pid = self.pid
            print('    Task started: %s on PID %d'%(str(task), self.pid))
            task.run()
            print('    Task end: %s on PID %d'%(str(task), self.pid))
            state.add_finished_task(task)
            task = state.get_task()
        print('    Process %d is done.'%self.pid)
        self.dp_state.num_processes.value -= 1
