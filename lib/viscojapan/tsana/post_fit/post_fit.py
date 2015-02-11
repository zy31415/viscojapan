import numpy as np

from ..pre_fit import LinResReader
from ..config_reader import ConfigReaderPostSec, ConfigReaderJumps

from ...constants import t_eq

from .tsmodel import *

__all__ = ['PostFit']

def est_am(t,y):
    """ Estimate a initial value for exponentials.
"""
    ch=t>t_eq
    y1=y[ch]
    return y1[-1]-y1[0]

class PostFit(object):
    def __init__(self,
                 site,
                 ):
        self.site = site

        self._load_post_sec()

        self._load_jumps()
        
        self._load_time_series_data()

    def _load_time_series_data(self):
        self.data = {}
        for cmpt in 'enu':
            reader = LinResReader(self.site, cmpt)
            self.data['%s'%cmpt] = self._generate_data(
                reader.t,
                reader.y,
                reader.ysd)

    def _generate_data(self, t, y, ysd):
        data = Data()
        data.t = t
        data.y0 = y
        data.y0_sd = ysd        
        data.cut(self.post_sec)
        return data

    def _load_post_sec(self):
        self.post_sec = ConfigReaderPostSec().read(self.site)        

    def _load_jumps(self):
        self.jumps = ConfigReaderJumps().read(
            self.site,
            tcuts = [(t_eq, np.inf)],
            )

    def gen_cfs(self, cmpts, post_model):       
        cf_list=[]            
        for cmpt in cmpts:
            func = Fc()
            f_cos = SubFcEq()
            f_cos.T0 = t_eq
            f_cos.jump = self._estimate_init_co(cmpt)
            f_cos.tag='TOHOKU'
            func.add_subf(f_cos)

            func.cmpt=cmpt.upper()
            nth=1
            for jump in self.jumps:
                f_jump=SubFcJump()
                f_jump.T0=jump
                f_jump.jump=.001
                f_jump.tag='JUMP_%d'%nth
                func.add_subf(f_jump)
                nth+=1
            
            _am = self._estimate_init_am(cmpt)
            
            if post_model == 'EXP':
                f_exp=SubFcEXP()
                f_exp.T0=t_eq
                f_exp.am= _am
                f_exp.tau=20.
                f_exp.tag='EXP'
                func.add_subf(f_exp)

            elif post_model == '2EXPs':
                f_exp1=SubFcEXP()
                f_exp1.T0=t_eq
                f_exp1.am=_am
                f_exp1.tau=10.
                f_exp1.tag='EXP1'
                func.add_subf(f_exp1)

                f_exp2=SubFcEXP()
                f_exp2.T0=t_eq
                f_exp2.am=_am*10.
                f_exp2.tau=1000.
                f_exp2.tag='EXP2'
                func.add_subf(f_exp2)
            
            cf = IndepMLReg()
            cf.func = func
            cf.data = self.data[cmpt]
            cf.SITE = self.site+'-res'
            cf.CMPT = cmpt
            cf_list.append(cf)
        
        cfs = JointMLReg(cf_list)
        cfs.SITE = self.site
        cfs.max_step = 1000
        cfs.post_model = post_model
        cfs.cmpts = cmpts

        return cfs

    def _estimate_init_co(self, cmpt):
        y = self.data[cmpt]._y0
        return np.mean(y)

    def _estimate_init_am(self, cmpt):
        y = self.data[cmpt]._y0
        return y[-1]-y[0]
        
