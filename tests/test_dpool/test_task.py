from time import sleep
from random import randrange

from viscojapan.dpool.dpool import DPool, Task

tasks = []

for n in range(20):
    tasks.append(Task(target = sleep,
                      args = (randrange(10),)))
print(tasks[0])
