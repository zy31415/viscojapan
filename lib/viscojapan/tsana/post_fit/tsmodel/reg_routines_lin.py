__all__ = ['LinIndepReg']

from .reg_models import IndepRegMod
from numpy import dot,diag
from numpy.linalg import solve, inv

class LinIndepReg(IndepRegMod):
    """
"""    
    # override
    def go(self):
        Jac = self.func.Jac(self.data._t)
        for ii in range(0,Jac.shape[0]):
            Jac[ii,]/=self.data._y0_sd

        L=dot(Jac,Jac.transpose())
        self.L = L
        self.R = dot(Jac,self.data._y0/self.data._y0_sd)
        ##self.R = self.R[:,0]
        res = solve(self.L,self.R)
        org = self.func.get_ps()
        self.func.ck_parsupdate(res-org)
        self.func.parsupdate(res-org)

    def uncertainty(self):
        Jac = self.func.Jac(self.data._t)
        for ii in range(0,Jac.shape[0]):
            Jac[ii,]/=self.data._y0_sd
        self.cov_1=dot(Jac,Jac.transpose())
        
        self.cov = inv(self.cov_1)

        self.uncer = diag(self.cov)

        n = 0
        for subf in self.func:
            for pn in subf.ipns:
                setattr(subf,pn+'_sd',self.uncer[n])
                n+=1
