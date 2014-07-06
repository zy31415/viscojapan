from time import sleep
from multiprocessing import Process
from os.path import join
import unittest

from viscojapan.dpool.running_proc_list import running_proc_list
from viscojapan.test_utils import MyTestCase

class Test_running_proc_list(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_append_and_pop(self):
        pl = running_proc_list(log_file=join(self.outs_dir, 'log'))
        pl.append_and_start(sleep, args=(10,))
        p = pl.pop_and_terminate()

    def test_clean_dead(self):
        pl = running_proc_list(log_file=join(self.outs_dir, 'log_clean'))
        pl.append_and_start(sleep, args=(.1,))
        sleep(1)
        dead = pl.pop_dead()
        self.assertEqual(len(pl),0)

if __name__=='__main__':
    unittest.main()


