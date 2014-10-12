import unittest
from os.path import join, exists
from os import makedirs

from .utils import overrides, get_this_script_dir

__all__ = ['MyTestCase']

class MyTestCase(unittest.TestCase):
    @overrides(unittest.TestCase)
    def setUp(self):
        self.this_script_dir = get_this_script_dir(self.this_script)

    @property
    def share_dir(self):
        return join(self.this_script_dir, 'share/')

    @property
    def outs_dir(self):
        path = join(self.this_script_dir, '~outs/')
        if not exists(path):
            makedirs(path)
        return path
    
