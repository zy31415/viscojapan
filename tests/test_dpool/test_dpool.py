import unittest
from time import sleep
from random import randrange
from os.path import join

from viscojapan.test_utils import MyTestCase
from dpool.dpool import DPool, Task

class Test_DPool(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test(self):
        tasks = []
        for n in range(5000):
            tasks.append(Task(target = sleep,
                              args = (randrange(20),)))
        dp = DPool(
            tasks=tasks,
            controller_file = join(self.share_dir, 'pool.config.dynamic')
            )
        dp.run()

if __name__ == '__main__':
    unittest.main()
        
