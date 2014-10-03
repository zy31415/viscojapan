from multiprocessing import Process

class Feeder(Process):
    def __init__(self, tasks, dp_state):
        super().__init__()
        self.tasks = tasks
        self.dp_state = dp_state        

    def run(self):
        for task in self.tasks:
            self.dp_state.q_waiting.put(task)
        
        
