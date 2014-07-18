from multiprocessing import Process

class DPoolProcess(Process):
    def __init__(self, dp_state):
        super().__init__()
        self.dp_state = dp_state

   
    def run(self):
        state = self.dp_state
        task = state.get_task()
        while task is not None:
            task.pid = self.pid
            state.add_running_task(self.pid, task)
            print('    Task started: %s on PID %d'%(str(task), self.pid))
            task.run()
            print('    Task end: %s on PID %d'%(str(task), self.pid))
            state.add_finished_task(task)
            task = state.get_task()
        print('    Process %d is done.'%self.pid)
        state.add_running_task(self.pid, 'Done')
