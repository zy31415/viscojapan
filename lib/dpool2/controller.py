'''
Controller file format:

# This config file is used to control the dynamic pool.
# 1st column,if_fix, 0-False, dynamic pool; 1-True, static pool
#
# if if_fix == 0 (False)
# 2st column, load, threashold of number of cpus left to load a task
# 3nd column, kill, threashold of number of cpus left to kill tasks
# 4rd column, sleep, sleep time for the next check in sec.
#
# if if_fix == 1 (True)
# 2st column, number of processes
# 3nd column, Not used,
# 4rd column, sleep, sleep time for the next check in sec.
#
# if_fix load  kill  sleep(sec)
0  1.5  0.5  2
#
# if_fix nproc NONE sleep(sec)
# 1 10 None 2
'''
import warnings
import time

import psutil as ps
import numpy as np

from .utils import next_non_commenting_line, _assert_file_exists

def assert_num_process(np):
    assert np>0
    ncpu = ps.cpu_count()
    if np > ncpu:
        warnings.warn("# processes (%d) > # cpu (%d)"%(np, ncpu))

class Controller(object):
    def __init__(self,
                 controller_file = 'pool.config'):
        self.controller_file = controller_file
        _assert_file_exists(self.controller_file)
        self.update()
        
    def update(self):
        tp = np.loadtxt(self.controller_file)
        assert tp.shape == (4,)
        if tp[0] == 0:
            self._if_fix = False
            self._threshold_load = tp[1]
            self._threshold_kill = tp[2]
            self._sleep_interval = tp[3]

            self._num_processes = None

        elif tp[0] == 1:
            self._if_fix = True
            self._num_processes = tp[1]
            assert_num_process(self._num_processes)
            self._sleep_interval = tp[3]

            self._threshold_load = None
            self._threshold_kill = None
        else:
            raise ValueError('File error.')

    @property
    def threshold_load(self):
        return self._threshold_load

    @property
    def if_fix(self):
        return self._if_fix

    @property
    def threshold_kill(self):
        return self._threshold_kill

    @property
    def sleep_interval(self):
        return self._sleep_interval

    @property
    def num_processes(self):
        return self._num_processes

    def sleep(self):
        time.sleep(self.sleep_interval)

    def update_and_sleep(self):
        self.update()
        self.sleep()

    def __str__(self):
        out = "Pool config: \n"
        if self.if_fix:
            out += '    Static: nproc = %.1f, sleep = %d\n'%\
                   (self.num_processes,self.sleep_interval)
        else:
            out += '    Dynamic: load = %.1f, kill = %.1f, sleep = %d'%\
                   (self.threshold_load,self.threshold_kill,self.sleep_interval)
        return out

