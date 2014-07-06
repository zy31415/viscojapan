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
from time import sleep

import psutil as ps

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

        self._first_time_update()

    def _parse_dynamic_pool_pars(self, pars):
        assert len(pars) == 3, '#parameters is wrong.'
        
        load = float(pars[0])
        assert load > 0
        
        kill = float(pars[1])
        assert kill > 0
        
        assert load > kill, 'load(=%d) should larger than kill(=%d)!'%(load, kill)    

        sleep = int(pars[2])
        assert sleep > 0
        
        self.threshold_load = load
        self.threshold_kill = kill
        self.sleep_interval = sleep
        
    def _parse_static_pool_pars(self, pars):
        assert len(pars) == 3
        
        nprocess=int(pars[0])
        assert_num_process(nprocess)
        self.num_processes = nprocess

        sleep=int(pars[2])
        assert sleep > 0
        self.sleep_interval = sleep

    def _parse_line(self, ln):
        pars = ln.strip().split()
        assert len(pars) == 4
        if_fix = int(pars[0])
        self.if_fix = if_fix

        if if_fix == 0:
            self._parse_dynamic_pool_pars(pars[1:])
        elif if_fix == 1:
            self._parse_static_pool_pars(pars[1:])
        else:
            raise ValueError('Unreconginzed inputs.')

    def _first_time_update(self):
        with open(self.controller_file) as fid:
            ln = list(next_non_commenting_line(fid))

        assert len(ln) == 1, 'File error: multiple entries.'
        self._parse_line(ln[0])
        
    def update(self):
        self._first_time_update()
        sleep(self.sleep_interval)

    def __str__(self):
        out = "Pool config: \n"
        if self.if_fix:
            out += '    Static: nproc = %.1f, sleep = %d\n'%\
                   (self.num_processes,self.sleep_interval)
        else:
            out += '    Dynamic: load = %.1f, kill = %.1f, sleep = %d'%\
                   (self.threshold_load,self.threshold_kill,self.sleep_interval)
        return out

