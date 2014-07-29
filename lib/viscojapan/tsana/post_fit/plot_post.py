try:
    from pylab import plt
except ImportError as err:
    pass

from numpy import linspace

_adj_dates=678577 
cs='bgrcmyk'

def plot_func(func,t):
    n=0
    for f in func.subfcs:
        plt.plot_date(t+_adj_dates,f(t),marker=None,ls='--',color=cs[n%len(cs)],label=f.tag)
        n+=1
    plt.plot(t+_adj_dates,func(t),color='r',linewidth=2)
               
def plot_cf(cf, color):
    t = cf.data.t
    y0 = cf.data.y0
    plt.plot_date(t+_adj_dates,y0,'x',label=cf.SITE+cf.CMPT,
              color='light'+color)
    plt.plot_date(cf.data._t+_adj_dates,
              cf.data._y0,'x',label=cf.SITE+cf.CMPT,
              color=color)
    t1 = min(t)
    t2 = max(t)
    ls=200
    plot_func(cf.func,linspace(t1,t2,ls))
    plt.title(cf.SITE+'-'+cf.CMPT)
    plt.gcf().autofmt_xdate()
    
def plot_post(cfs,ifshow=False,loc=2):
    for cf in cfs:
        plot_cf(cf, color='blue')
        plt.legend(loc=loc)
        if ifshow:
            plt.show()
