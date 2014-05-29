from greaer import GReader

class DiffG(object):
    ''' This class computes the diffrence of G with respcet to (wrt)
an indicated variable.
'''
    def __init__(self, fG1, fG2, wrt):
        ''' Note:
wrt - with respect to, variable that the change WRT.
'''
        self.fG1 = fG1
        self.fG2 = fG2
        self.wrt = wrt

        self.G1_reader = GReader(self.fG1)
        self.G2_reader = GReader(self.fG2)

        self._get_vars()

    def _get_vars(self):
        with h5py.File(self.G1) as fid:
            self.var1 = fid['/info/%s'%self.wrt]
            setattr(self, self.wrt+'1', self.var1)

        with h5py.File(self.G2) as fid:
            self.var2 = fid['/info/%s'%self.wrt]
            setattr(self, self.wrt+'2', self.var2)

    def get(self, day):
        G1 = self.G1_reader(day)
        G2 = self.G2_reader(day)

        dG = (G2 - G1)/(self.var2 - self.var1)

        return dG
        
