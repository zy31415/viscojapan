import unittest
from os.path import join

from viscojapan.dpool.controller import  Controller
from viscojapan.test_utils import MyTestCase

class TestController(MyTestCase):
    def setUp(self):
        self.this_script = __file__
        super().setUp()

    def test_dynamic_pool(self):
        con = Controller(
            controller_file = join(self.share_dir,'pool.config.dynamic')
            )
        con.update()

        self.assertEqual(con.threshold_load, 1.5)
        self.assertEqual(con.threshold_kill, 0.5)
        self.assertEqual(con.sleep_interval, 2)

    def test_static_pool(self):
        con = Controller(
            controller_file = join(self.share_dir,'pool.config.static')
            )
        con.update()

        self.assertEqual(con.num_processes, 10)
        self.assertEqual(con.sleep_interval, 2)
        

if __name__== '__main__':
    unittest.main()
