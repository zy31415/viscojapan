from pylab import *
from os.path import basename
__all__ = ['read_tenv_ts','read_tenv_tssd','read_tenv_t','plot_tenv_ts']

_ts_data_type=dtype("a4,a7,f,i,i,i,(1,3)f8,f,(1,3)f8,f,f")

def file_len(fname):
    ''' Count the number of lines in a file.
'''
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def read_tenv_ts(f,cmpt):
    """Fetch time series of a site form database.

    Keyword arguments:
    site -- site name
    cmpt -- type of time series, can be any one of these:
        e, n, u        
    """
    tp=loadtxt(f,_ts_data_type)
    ln=file_len(f)
    if ln==0:
        raise ValueError('Empty File!')
    elif ln==1:
        tp=[tp.item()]
    if cmpt=='e':
        return array([n[6][0][0] for n in tp])
    if cmpt=='n':
        return array([n[6][0][1] for n in tp])
    if cmpt=='u':
        return array([n[6][0][2] for n in tp])
    raise ValueError('Wrong cmpt!')

def read_tenv_tssd(f,cmpt):
    """Fetch standard deviation of time series of a site form database.

    Keyword arguments:
    site -- site name
    cmpt -- type of time series, can be any one of these:
        e, n, u
        
    """
    tp=loadtxt(f,_ts_data_type)
    ln=file_len(f)
    if ln==0:
        raise ValueError('Empty File!')
    elif ln==1:
        tp=[tp.item()]
    if cmpt=='e':
        return array([n[8][0][0] for n in tp])
    if cmpt=='n':
        return array([n[8][0][1] for n in tp])
    if cmpt=='u':
        return array([n[8][0][2] for n in tp])
    raise ValueError('Wrong cmpt!')

def read_tenv_t(f,ttype):
    """Fetch time epoch from a tenv file.

    Keyword arguments:
    f - file
    ttype -- type of time epoch, can be any one of these:
        mjd, std, dyr
        
    """
    tp=loadtxt(f,_ts_data_type)
    ln=file_len(f)
    if ln==0:
        raise ValueError('Empty File!')
    elif ln==1:
        tp=[tp.item()]
    if ttype=='std':
        return asarray([n[1].decode('utf-8') for n in tp])
    if ttype=='dyr':
        return array([round(n[2],4) for n in tp],dtype='float')
    if ttype=='mjd':
        return array([int(n[3]) for n in tp],dtype='int')
    raise ValueError('Wrong ttype!')

_adj_dates=678577
def plot_tenv_ts(f,eb=True):
    ''' Plot a tenv file.
eb - if with errorbars
'''
    t=read_tenv_t(f,'mjd')
    e=read_tenv_ts(f,'e')
    n=read_tenv_ts(f,'n')
    u=read_tenv_ts(f,'u')
    esd=read_tenv_tssd(f,'e')
    nsd=read_tenv_tssd(f,'n')
    usd=read_tenv_tssd(f,'u')

    t+=_adj_dates

    site=basename(f)
    if eb:
        errorbar(t,e,yerr=esd,fmt='r.',label='%s-%s'%(site,'e'))
        errorbar(t,n,yerr=nsd,fmt='b.',label='%s-%s'%(site,'n'))
        errorbar(t,u,yerr=usd,fmt='g.',label='%s-%s'%(site,'u'))
        gca().xaxis_date()
    else:
        plot_date(t,e,'rx',label='%s-%s'%(site,'e'))
        plot_date(t,n,'bx',label='%s-%s'%(site,'n'))
        plot_date(t,u,'gx',label='%s-%s'%(site,'u'))

    ax=gca()
    # Set major x ticks on Mondays.
##    ax.xaxis.set_major_locator(
##        D.AutoDateLocator()
##        )
##    ax.xaxis.set_major_formatter(
##        D.DateFormatter('%d %b %Y')
##        )
    gcf().autofmt_xdate()

    grid('on')
    ylabel('Meter')
    xlabel('Date')
    title(site)

if __name__ == "__main__":
    a= read_tenv_t('J064','std')
