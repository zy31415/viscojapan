from multiprocessing import Process

class DPoolProcess(Process):
    def __init__(self, dp_state):
        super().__init__()
        self.dp_state = dp_state

    def start(self):
        super().start()
        self.dp_state.register_running_tasks(self.pid)
    
    def run(self):
        state = self.dp_state
        while state.if_has_more_task():                
            task = state.pop_task()
            task.pid = self.pid
            state.update_running_tasks(self.pid, task)
            task.run()            
            state.register_finished_task(task)

        state.unregister_running_tasks(self.pid)
