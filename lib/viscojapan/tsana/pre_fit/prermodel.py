'''Do linear regresion for pre-seismic time series.
@author Yang Zhang
'''
from rpy2.robjects import FloatVector,BoolVector,globalenv,Formula
from rpy2.robjects import r as _r
from pylab import *

__all__=['PreRModel','_r']

def cut_ts(t,tcuts):
    ''' Return logical indexing of epochs indicated by tcuts.
'''
    ch = asarray(zeros_like(t),'bool')
    for cut in tcuts:
        t1=cut[0]
        t2=cut[1]
        ch = ch | ((t>t1) & (t<t2))
    return ch


class PreRModel():
    ''' This class do linear regression on preseismic time series using R.
Usage:
Set the following parameters:
- Linear Model parameters:
    if_sea
    if_semi
    jumps
    outlier_cri
    
- Data parameters:
    t
    y
    lin_secs
'''
    def __init__(self):
        # initialize the r process
        _r('''
            # define a heaviside function:
            hvsd <-
            function(x, a = 0){
                result = (sign(x-a) + 1.)/2.
                result
            }

            T<-365.
            Omega<-2*pi/T
            ''')
        ## @var if_sea
        # If consider seasonal signal?
        self.if_sea=None

        ## @var if_semi
        # if consider semisesonal signal?
        self.if_semi=None

        ## jumps list
        self.jumps=None

        ## data_par : t
        self.t=None

        ## y
        self.y=None

        ## ysd
        self.y=None

        ## linear sections used for linear regression.
        self.linsecs=None

        ## record the outliers
        self.if_outlier=None

        ## outlier criteri (times of st):
        self.outlier_cri=3.0
        

    def form_model(self):
        ''' Form a linear model for lm command and store in the R process.
'''
        formula='y~1+t'
        assert self.if_sea is not None, "If using seasonal model?"
        assert self.if_semi is not None, "If using semi-seasonal model?"
        assert self.jumps is not None, "Is there any jumps?"
        
        if self.if_sea:
            formula+='+sin(Omega*t)+cos(Omega*t)'
        if self.if_semi:
            formula+='+sin(2.*Omega*t)+cos(2.*Omega*t)'
        for jump in self.jumps:
            formula+='+hvsd(t,%d)'%jump

        ## R model formula string
        self.fml_str=formula
        
        globalenv['fml']=Formula(formula)

    def form_subset(self):
        ''' Form the subset parameter for lm model.
Consider:
(1)linear sections
(2) Outliers
'''
        assert self.t is not None, "t is not defined."
        subset=cut_ts(self.t,self.linsecs)

        # consider outliers:
        if self.if_outlier is None:
            self.if_outlier = asarray(zeros_like(self.t),'bool')
        else:
            subset = subset & (~self.if_outlier)

        self.subset=subset
        globalenv['subset']=BoolVector(subset)
        
    def form_data(self):
        ''' Form time series data used in lm model.
'''
        assert self.t is not None, "t is not defined."
        assert self.y is not None, "y is not defined."

        globalenv['t']=FloatVector(self.t)
        globalenv['y']=FloatVector(self.y)
        if self.ysd is None:
            globalenv['ysd']=FloatVector(ones_like(self.y))
        else:
            globalenv['ysd']=FloatVector(self.ysd)
        _r('the_data <- data.frame(t=t,y=y,ysd=ysd)')

    def get_res(self):
        ''' Return residual of the part of time series that is used in linear regression.
Nan is there is no residula available.
'''
        tp=asarray(_r('resid(fit)'))
        res=zeros_like(self.t)+nan
        res[self.subset]=tp
        return res

    def predict(self,t,level=0.95,interval='none'):
        ''' Interface of R predict function.
'''
        globalenv['t_pred']=FloatVector(t)
        y=array(_r('predict(fit,data.frame(t=t_pred),level=%f,interval="%s")'%\
                   (level,interval)))
        return y

    def predict_res(self,t,y,level=0.95):
        y_pred=self.predict(t=t,level=level)
        return y-y_pred
        

    def get_res_std(self):
        ''' Return standard error of residuls.
'''
        return float(_r("summary(fit)$sigma")[0])
    
    def find_outliers(self,verbose=True):
        ''' Detect outliers based on last linear regrssion.
and mark the if_outlier array.
Return:
Logic index indicating outliers.
'''
        std=self.get_res_std()
        cri=std*self.outlier_cri
        res=self.get_res()
        ch=abs(res)>cri
        return ch

    def mark_outliers(self):
        ''' Mark if_outlier array. Return number of outliers
'''
        ch=self.find_outliers()
        self.if_outlier[ch]=True
        return sum(ch)

    def lm(self,verbose=True):
        ''' Do linear regression.
'''
        self.form_model()
        self.form_data()
        self.form_subset()
        _r('fit <- lm(fml,the_data,subset)')
        nth=1
        if verbose:
            print('%dth iter: std(mm)=%.3f vel(mm/yr)=%.3f outliers #:%d'%\
                  (nth,self.get_res_std()*1000.,self.get_vel()*365.*1000.,
                   sum(self.if_outlier)))
        nth+=1
        while self.mark_outliers()>0:
            self.form_subset()
            #_r('fit <- lm(fml,the_data,subset,weights=1/ysd^2)')
            _r('fit <- update(fit,.~.,subset=subset,weights=1/ysd^2)')
            if verbose:
                print('%dth iter: std(mm)=%.3f vel(mm/yr)=%.3f outliers #:%d'%\
                      (nth,self.get_res_std()*1000.,self.get_vel()*365.*1000.,
                       sum(self.if_outlier)))
            nth+=1

    def get_vel(self):
        '''
'''
        return _r("fit$coe[['t']]")[0]

    def get_vel_sd(self):
        '''
'''
        return _r("summary(fit)$coef['t','Std. Error']")[0]

    def get_jumps(self):
        ''' Reture jumps and their value.
'''
        for jump in self.jumps:
            yield (jump,_r("fit$coe[['hvsd(t, %d)']]"%jump)[0])


if __name__=='__main__':
        
    mod=PreRModel()

    # model:
    mod.if_sea=True
    mod.if_semi=True
    mod.jumps=[]

    # data:
    tp=loadtxt('../J550.IGS08')
    t=tp[:,0]
    e=tp[:,1]*1000.

    t_eq=55631

    mod.t=t
    mod.y=e
    mod.linsecs=[[-inf, 55631]]

    mod.lm()
    print(_r('summary(fit)'))
    print(_r('coef(summary(fit))'))

    plot(mod.t,mod.get_res(),'x')
    res=mod.predict_res(mod.t[mod.if_outlier],mod.y[mod.if_outlier])
    plot(mod.t[mod.if_outlier],res,'r.')
    show()
