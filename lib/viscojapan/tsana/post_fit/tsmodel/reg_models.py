__all__ = ['RegMod','IndepRegMod','JointRegMod']

from numpy import sqrt, mean
import numpy as np

class RegMod():
    """ Interface.
The combination of data and func.
Caculations based on both data and func at the same time are defined in this class.
"""
    def __init__(self):
        pass

    def ndata(self):
        raise NotImplementedError

    def np(self):
        raise NotImplementedError
    
    def upsilon(self):
        """ Return the degree of freedom of the regression system."""
        return self.ndata() - self.np()

    def chisq(self):
        """ Misfit: chi-squre"""
        raise NotImplementedError

    def re_chisq(self):
        """ Misfit: reduced chi-squre"""
        raise NotImplementedError

    def rms(self):
        """ Misfit: RMS"""
        raise NotImplementedError

 
class IndepRegMod(RegMod):
    """ A data+function combo for independent regression method.
"""
    def __init__(self):
        RegMod.__init__(self)

        self.data = None
        self.func = None
        
        self.SITE = None
        self.CMPT = None

    # override
    def ndata(self):
        return len(self.data)

    # override
    def np(self):
        return self.func.get_np()

    # override
    def chisq(self):
        """ Return chi-square.
"""
        res = (self.func(self.data._t)-self.data._y0)/self.data._y0_sd
        res = (res**2).sum()
        return res

    # override
    def re_chisq(self):
        """ Return reduced chi-square.
"""
        return self.chisq() / self.upsilon()

    # override
    def rms(self):
        """ Return rms.
"""
        return sqrt(mean((self.func(self.data._t)-self.data._y0)**2))

    def set_data(self, data):
        """ Set data.
"""
        self.data = data
        self.SITE = data.SITE
        self.CMPT = data.CMPT

    def set_func(self, func):
        """ Set func.
"""
        self.func = func

    def set_data_func(self, xxx_todo_changeme):
        """ Set data and func.
"""
        (data, func) = xxx_todo_changeme
        for tp1, tp2 in zip((self.set_data,self.set_func),(data,func)):
            tp1(tp2)

    def residual(self):
        """ Return the residual between data and model.
"""
        return self.data.y0 - self.func(self.data.t)

# forwarding
    def get_cps(self):
        return self.func.get_cps()

    def get_cpns(self):
        return self.func.get_cpns()

    def get_cpftags(self):
        return self.func.get_cpftags()

    def get_p(self, pn, ftag = []):
        return self.func.get_p(pn, ftag)

    def get_subf(self, tag):
        return self.func.get_subf(tag)

    def __str__(self):
        out = 'IndepRegMod object: %s.%s\n'%(self.SITE, self.CMPT)
        out += '    Misfit:\n'
        out += '        chisq = %g\n'%(self.chisq())
        out += '        re_chisq = %g\n'%(self.re_chisq())
        out += '        rms = %g mm\n'%(self.rms()*1000.)
        tp =  self.func.__str__()
        tp = tp.split('\n')
        for line in tp:
            out += '    '+line+'\n'
        return out    

class JointRegMod(RegMod):
    """ A data-function combo model for joint regression method.
"""
    def __init__(self,cfs,csz = None):
        RegMod.__init__(self)
        self.cfs = cfs
        if csz == None:
            self.csz = cfs[0]._func.get_ncp()
        else:
            self.csz = csz

    def __iter__(self):
        """ Iterator.
"""
        for cf in self.cfs:
            yield cf                

    # override
    def ndata(self):
        res = 0
        for cf in self.cfs:
            res += cf.ndata()
        return res

    # override
    def np(self):
        res  = 0
        for cf in self.cfs:
            res += (cf.np() - self.csz)
        res += self.csz
        return res

    # override
    def chisq(self):
        res=0.0
        for cf in self.cfs:
            res += cf.chisq()
        return res

    # override
    def re_chisq(self):
        return self.chisq() / self.upsilon()

    # override
    def rms(self):
        N = self.ndata()
        res = 0.
        for cf in self.cfs:
            res += ((cf.rms())**2)*cf.ndata()
        return sqrt(res/N)

    def get_cps(self):
        return self[0].get_cps()

    def get_cpns(self):
        return self[0].get_cpns()

    def get_cpftags(self):
        return self[0].get_cpftags()        

    def cut(self, tcuts):
        for cf in self.cfs:
            cf.data.cut(tcuts)

    def get_cf(self, SITE,CMPT=[]):
        """ Return IndepRegMod objects by search them by their SITE and CMPT tags
in the JointRegMod object.
"""
        out = []
        for cf in self:
            if cf.SITE==SITE:
                if CMPT==[]:
                    out.append(cf)
                elif CMPT==cf.CMPT:
                    out.append(cf)
        if len(out)==1:
            return out[0]
        return out

    def __getitem__(self,inpar):
        """ Overloading [] operator.
"""
        if isinstance(inpar,int) or isinstance(inpar,slice):
            return self.cfs[inpar]
        if isinstance(inpar,str):
            tp = inpar.split('-')
            site = tp[0]
            cmpt = tp[1]
            return self.get_cf(site,cmpt)

    def del_cf(self, SITE, CMPT=[]):
        """ Delete a IndepRegMod object in the JointRegMod object by their
SITE and CMPT tags.
"""
        fordel = self.get_cf(SITE, CMPT)
        for tp in fordel:
            self.cfs.remove(tp)

    def aic(self):
        '''
AIC = 2*k - 2*ln(L)
    = 2*k + p*ln(2*pi) + ln|Sig| + \
      (G(m)-d)^T * Sig^-1 * (G(m)-d)

where k - number of parameters
      L - likelyhood
      p - number of data
      Sig - sigma matrix

Ref:
For Likelyhood defination:
    Johnson, Applied multivariate statistical analysis, p150
'''
        num_pars = self.np()
        num_data = self.ndata()
    
        ysd = []
        for cf in self:
            ysd.append(cf.data._y0_sd)
        ysd = np.asarray(ysd).flatten()        
            
        aic = 2*num_pars + num_data*np.log(2*np.pi) + \
              np.log(ysd**2).sum() + \
              self.chisq()
        return aic
        
        
