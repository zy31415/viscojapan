import unittest
from os.path import join
import warnings

from numpy import arange
from numpy.testing import assert_almost_equal
from pylab import plt

from viscojapan.fault.fault_framework import FaultFramework
from viscojapan.utils import get_this_script_dir

this_test_path = get_this_script_dir(__file__)

class TestFaultFramework(unittest.TestCase):
    def setUp(self):
        self.fm = FaultFramework()

    def test(self):
        plt.plot(self.fm.XG, self.fm.DEP, '-o')
        plt.axis('equal')
        plt.axhline(0, color='black')
        plt.gca().set_yticks(self.fm.DEP)
        plt.gca().set_xticks(self.fm.XG)
        plt.grid('on')
        plt.title('Ground x versus depth')
        plt.xlabel('Ground X (km)')
        plt.ylabel('depth (km)')

        for xi, yi, dip in zip(self.fm.XG, self.fm.DEP, self.fm.DIP_D):
            plt.text(xi, yi, 'dip = %.1f'%dip)
        
        plt.savefig(join(this_test_path,'dep_XG.png'))
        plt.close()

    def test_dip(self):
        xf = arange(0, 425)
        dips = self.fm.get_dip(xf)
        plt.plot(xf,dips)
        plt.grid('on')
        plt.gca().set_xticks(self.fm.XG)
        plt.ylim([0, 30])
        plt.savefig(join(this_test_path, 'xf_dips.png'))
        plt.close()

    def test_dep(self):
        xf = arange(0, 425)
        deps = self.fm.get_dep(xf)
        plt.plot(xf,deps)

        plt.gca().set_yticks(self.fm.DEP)
        plt.gca().set_xticks(self.fm.XG)
        
        plt.grid('on')
        plt.title('Ground x versus depth')
        plt.xlabel('Ground X (km)')
        plt.ylabel('depth (km)')
        plt.axis('equal')
        plt.savefig(join(this_test_path, 'xf_deps.png'))
        plt.close()

    def test_xfault_to_xground(self):
        self.assertRaises(AssertionError,
                          self.fm.xfault_to_xground, [500])
        self.assertRaises(AssertionError,
                          self.fm.xfault_to_xground, [-0.1])
        xf = arange(0, 425)
        xg = self.fm.xfault_to_xground(xf)

    def test_xground_to_xfault(self):
        self.assertRaises(AssertionError,
                          self.fm.xground_to_xfault, [500])
        self.assertRaises(AssertionError,
                          self.fm.xground_to_xfault, [-0.1])
        xg = arange(0, 393)
        xf = self.fm.xground_to_xfault(xg)

    def test_xground_xfault_conversion(self):
        xf = arange(0, 425)
        xg = self.fm.xfault_to_xground(xf)
        xf1 = self.fm.xground_to_xfault(xg)

        assert_almost_equal(xf, xf1)

    def test_get_xf_by_dep_scalar(self):
        for nth, dep in enumerate(self.fm.DEP):
            xf = self.fm.get_xf_by_dep_scalar(dep)
            assert_almost_equal(xf, self.fm.XF[nth])


if __name__ == '__main__':
    unittest.main()
