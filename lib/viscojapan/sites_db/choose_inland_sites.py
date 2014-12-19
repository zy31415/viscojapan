import numpy as np

__all__ = ['choose_inland_GPS',
           'choose_inland_GPS_cmpts_for_all_epochs',
           'choose_inland_GPS_cmpts_at_nth_epochs',
           ]

def choose_inland_GPS(sites):
    ch = []
    for site in sites:
        if isinstance(site, bytes):
            site = site.decode()
        if site[0]=='_':
            ch.append(False)
        else:
            ch.append(True)
    return np.asarray(ch,bool)

def choose_inland_GPS_cmpts_for_all_epochs(sites, num_epochs):
    ch = choose_inland_GPS(sites)
    out = np.asarray([[ch]*3]).T.flatten()
    out = np.asarray([out]*num_epochs).flatten()
    return out

def choose_inland_GPS_cmpts_at_nth_epochs(sites, nth_epoch, num_epochs):
    ch1 = choose_inland_GPS_cmpts_for_all_epochs(sites, num_epochs=1)
    ch2 = [False]*len(ch1)
    out = []

    for nth in range(num_epochs):
        if nth == nth_epoch:
            out.append(ch1)
        else:
            out.append(ch2)
    out = np.asarray(out).flatten()
    return out


