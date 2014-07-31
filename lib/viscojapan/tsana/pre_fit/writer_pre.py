from datetime import datetime

__all__=['Writer']

class Writer():
    ''' Output results of the linear regression to file.
'''
    def __init__(self,obj,file):
        ''' file is either a file name or file id.
'''
        self.obj=obj
        if isinstance(file,str):
            self.fid=open(file,'wt')
        else:
            self.fid=file
        self.title=None

    def write_header_model_pars(self):
        obj=self.obj
        fid=self.fid
        fid.write('# Model parameters:\n')
        fid.write('#     model: %s\n'%obj.fml_str)        
        for s in obj.linsecs:
            fid.write('#     linear sec: %.0f %.0f\n'%(s[0],s[1]))
        for j in obj.jumps:
            fid.write('#     jump: %.0f\n'%(j))

        fid.write('#     outlier cri (times of rms): %f\n'%obj.outlier_cri)
        
        fid.write('#\n')
        
    def write_header_results(self):
        obj=self.obj
        fid=self.fid
        fid.write('# Results summary:\n')
        fid.write('#     velocity (mm/yr): %.2f\n'%\
                  (obj.get_vel()*365.*1000.))
        fid.write('#     velocity sd (mm/yr): %.3f\n'%\
                  (obj.get_vel_sd()*365.*1000.))
        fid.write('#     std error (mm): %f\n'%(obj.get_res_std()*1000.))
        fid.write('#     rms (mm): %f\n'%(obj.get_res_rms()*1000.))

        for t,jump in obj.get_jumps():
            fid.write('#     jump %d (m): %f\n'%(t,jump))

        self._write_header_results_seasonal_semiseasonal(fid)            
        self._write_header_results_outliers(fid)

    def _write_header_results_seasonal_semiseasonal(self, fid):
        if self.obj.if_sea is not None:
            fid.write('#     seasonal magnitude(mm): %f\n'%\
                      (self.obj.get_magnitude_seasonal()*1000.))
        if self.obj.if_semi is not None:
            fid.write('#     semi-seasonal magnitude(mm): %f\n'%\
                      (self.obj.get_magnitude_semiseasonal()*1000.))

    def _write_header_results_outliers(self, fid):
        # outliers list
        outliers = self.obj.t[self.obj.if_outlier]
        fid.write('#     outliers (%d): '%(len(outliers)))
        for ol in outliers:
            fid.write('%d '%ol)
        fid.write('\n')
        fid.write('#\n')
            
    def write_header(self):
        obj=self.obj
        fid=self.fid
        fid.write('# %s\n'%self.title)
        fid.write('#\n')
        self.write_header_model_pars()
        self.write_header_results()        
        fid.write('# Date: %s\n'%(str(datetime.now())))
        fid.write('#\n')
        fid.write('# mjd   y(m)    yres(m)     ysd(m)\n')

    def write_ts(self):
        obj=self.obj
        for t,y,ysd,y_pred in zip(obj.t,obj.y,obj.ysd,obj.predict_res(obj.t,obj.y)):
            self.fid.write('%d %9.6f %9.6f %9.6f\n'%(t,y,y_pred,ysd))
            
            
    def write(self):
        self.write_header()
        self.write_ts()
        self.fid.close()
        
