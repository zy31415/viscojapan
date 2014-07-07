import time

def time_to_string(t):
    tstr = time.strftime("%H:%M", time.localtime(t))
    return tstr

class Task(object):
    def __init__(self,
                 target,
                 args = (),
                 kwargs = {}):
        self.target = target
        self.args = args
        self.kwargs = kwargs

        self.t_start = None
        self.t_end = None
        self.t_consumed = None
        self.pid = None

    def run(self):
        self.t_start = time.time()
        target = self.target
        args = self.args
        kwargs = self.kwargs
        res = target(*args, **kwargs)
        self.t_end = time.time()
        self.t_consumed = self.t_end - self.t_start
        return res

    def __str__(self):
        out = "  %s ("%self.target.__name__
        for arg in self.args:
            out += "%s, "%arg
        for key, arg in self.kwargs.items():
            out += "%s=%s, "%(key,arg)
        out += ")"
        if self.t_consumed is not None:
            out += '\n    in %.2f sec (from %s to %s)'%\
                   (self.t_consumed, time_to_string(self.t_start),
                    time_to_string(self.t_end))
            out += ' @ PID(%d)'%self.pid
        return out
