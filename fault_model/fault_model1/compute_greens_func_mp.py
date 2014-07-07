import glob
from os.path import basename

from viscojapan.pollitz.pollitz_wrapper import stat2gA
from dpool.dpool import DPool, Task

def func(file_flt):
    fn = basename(file_flt)
    cmd = stat2gA(
        earth_model_stat = 'share/earth.model_He50km',
        stat0_out = 'workspace/stat0.out',
        file_flt = file_flt,
        file_sites = 'share/sites_with_seafloor',
        file_out = 'outs_disp/out_'+fn,
        if_skip_on_existing_output = True,
        stdout = open('/dev/null', 'w')
        )
    cmd()

tasks = []

for f in sorted(glob.glob('workspace/subflts/flt_????')):
    tasks.append(Task(target = func,
                      args = (f,)))

dp = DPool(
    tasks=tasks,
    controller_file = 'pool.config'
    )

dp.run()
