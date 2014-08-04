from numpy import asarray

class ResidualWriter(object):
    def __init__(self, cfs):
        self.cfs = cfs
        
        self.site = cfs.SITE
        self.post_model = cfs.post_model
        self.component_code = cfs.component_code

    def _write_header_general_info(self,fid):
        fid.write('# number of epochs used : %d\n'%(self.cfs[0].ndata()))
        fid.write('# component code : %d\n'%self.cfs.component_code)
        fid.write('# post model : %s\n'%self.cfs.post_model)
        fid.write('# cycles (succ/all): %d/%d\n'%\
                  (self.cfs.ncyc_suc, self.cfs.ncyc_all))

    def _write_header_co(self, fid):
        fid.write('# CO(m) : %s\n'%(''.join([' %f'%co for co in self.cos])))

    def _write_header_post_for_EXP(self, fid):
        fid.write('# TAU EXP(day):%f\n'%(self.taus[0]))
        fid.write('# AM EXP(m): %s\n'%(''.join([' %f'%am for am in self.ams])))

    def _write_header_post_for_2EXPs(self, fid):
        fid.write('# TAU EXP1(day): %f \n'%(self.taus[0][0]))
        fid.write('# AM EXP1(m): %s \n'%\
                  (''.join([' %f'%am[0] for am in self.ams])))
        fid.write('# TAU EXP2(day): %f \n'%(self.taus[0][1]))
        fid.write('# AM EXP2(m): %s \n'%\
                  (''.join([' %f'%am[1] for am in self.ams])))

    def _write_header_post(self, fid):
        if self.post_model == 'EXP':
            self._write_header_post_for_EXP(fid)
        elif self.post_model == '2EXPs':
            self._write_header_post_for_2EXPs(fid)
        else:
            raise ValueError('Post model not recognized.')

    def _write_header_misfit(self, fid):
        fid.write('# CHISQ : %s\n'%\
                  (''.join([' %f'%ii for ii in self.chisqs])))
        fid.write('# RE_CHISQ : %s\n'%\
                  (''.join([' %f'%ii for ii in self.rechisqs])))
        fid.write('# RMS (mm) : %s\n'%\
                  (''.join([' %f'%ii for ii in self.rmses])))  

    def _write_header_array_header(self, fid):
        fid.write('# mjd  e_res(m)  n_res(m)  u_res(m)\n')

    def _write_residual_array(self, fid):
        ys = asarray([cf.residual() for cf in self.cfs],'float').transpose()
        Ts = self.cfs[0].data.t        
        for y,t in zip(ys,Ts):
            fid.write('%5d %s\n'%(t,''.join([' %13.6E'%ii for ii in y])))
##            fid.write('%5d %13.6E %13.6E %13.6E\n'%\
##                      (t, y[0], y[1], y[2]))

    def _write_header(self, fid):
        cos=[]
        ams=[]
        taus=[]
        chisqs = []
        rechisqs = []
        rmses = []
        for cf in self.cfs:
            cos.append(cf.get_p('jump','TOHOKU'))
            ams.append(cf.get_p('am'))
            taus.append(cf.get_p('tau'))
            rechisqs.append(cf.re_chisq())
            chisqs.append(cf.chisq())
            rmses.append(cf.rms())
        self.cos = cos
        self.ams = ams
        self.taus = taus
        self.rechisqs = rechisqs
        self.chisqs = chisqs
        self.rmses = rmses

        self._write_header_general_info(fid)
        self._write_header_co(fid)
        self._write_header_post(fid)
        self._write_header_misfit(fid)
        fid.write('#\n')
        self._write_header_array_header(fid)        
        
    def save(self, fn):
        with open(fn,'wt') as fid:
            self._write_header(fid)
            self._write_residual_array(fid)


