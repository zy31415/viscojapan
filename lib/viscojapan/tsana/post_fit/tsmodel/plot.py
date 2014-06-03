from pylab import *

__all__=['plot_func','plot_cf']

_adj_dates=678577 

cs='bgrcmyk'

def plot_func(func,t):
    plt.plot(t+_adj_dates,func(t),color='r',linewidth=3)

    n=0
    for f in func.subfcs:
        plt.plot_date(t+_adj_dates,f(t),marker=None,ls='-',color=cs[n%len(cs)],label=f.tag)
        n+=1
               
def plot_cf(cf):
    t = cf.data.t
    y0 = cf.data.y0
    plot_date(t+_adj_dates,y0,'x',label=cf.SITE+cf.CMPT)
    t1 = min(t)
    t2 = max(t)
    ls=200
    plot_func(cf.func,linspace(t1,t2,ls))
    title(cf.SITE+'-'+cf.CMPT)
    gcf().autofmt_xdate()

    
if __name__=='__main__':
    site='J167'
    plot_site(site)
    plot_jumps(site)
    plt.legend(loc=2)
    plt.show()
