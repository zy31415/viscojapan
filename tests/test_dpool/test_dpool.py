from time import sleep
from random import randrange

from dpool.dpool import DPool, Task

tasks = []

for n in range(20):
    tasks.append(Task(target = sleep,
                      args = (randrange(10),)))
dp = DPool(
    tasks=tasks,
    controller_file='share/pool.config.dynamic')

dp.run()
