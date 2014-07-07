from datetime import datetime, timedelta
from calendar import isleap
from numpy import asarray, ndarray, inf
from math import floor

__all__=['asmjd','asdyr','asstd','asdtype']
__doc__=\
"""
This module converts between three different time systems: std, mjd and dyr
mjd is used in internal storage and computation.
std is used for user reading.
dyr is usually used for plotting.
"""


class Date:
    """
This class defines the basic date formats conversions.
Functions defined in this class deals only the simplies situation:
They accept only scaler input and don't do any formats validity check.
More robust functions used in pratical computation are defined out of this class
by invoking routines defined in this classes.

Acronym conventions used here are:
std - STring Date
dyr - Decimal YeaR
mjd - Modified Julian Date

std <--> mjd <--> dyr
There are altogether six conversions but only four of them need to carefully defined in details.
Each of the other two (convertions between std and dyr) is equalized to other two conversions.

zy 02/27/12
"""
    # This is an global static class member
    epoch_MJD = datetime(1858,11,17,0,0,0) # the starting point of Modified Julian Day

    def std2mjd(self, std):
        """Converting from STring Date to Modified Julian Date.
String date is with the format "%y%b%d".

    zy, 03/15/11
    """
        tp = datetime.strptime(str(std),"%y%b%d")
        return int((tp - self.epoch_MJD).days)

    def mjd2std(self,mjd):
        """Converting from Modified Julian Date to STring Date. 
        String date is in the form "%y%b%d".
        zy, 03/15/11
        """
        return (self.epoch_MJD + timedelta(int(mjd))).strftime("%y%b%d").upper()

    def mjd2dyr(self,mjd):
        """Converting from Modified Julian Date to Decimal YeaR. 
        zy, 03/15/11
        """
        mjd = int(mjd)
        t0 = self.epoch_MJD + timedelta(mjd)
        yr0 = t0.year

        # find out the nearest leap year in the past.
        yr1 = yr0
        while not isleap(yr1):
            yr1 -= 1
        t1 = datetime.strptime(str(yr1)+"JAN01","%Y%b%d")

        days = (t0 - t1).days

        out = float(yr1) + float(days)*4.0/1461.
        return round(out,4)

    def dyr2mjd(self,dyr):
        """Converting from Decimal YeaR to Modified Julian Date. 
        zy, 02/27/12
"""
        dyr = round(dyr,4)
        yr0 = int(floor(dyr))

        # find out the nearest leap year in the past.
        yr1 = yr0
        while not isleap(yr1):
            yr1 -= 1
        t1 = datetime.strptime(str(yr1)+"JAN01","%Y%b%d")

        days = int((dyr - yr1)*1461./4.)
        t2 = t1 + timedelta(days)

        return int((t2 - self.epoch_MJD).days)
 
    
    def std2dyr(self,std):
        """Converting from STring Date to decimal year.
        String date is in the form "%y%b%d"
        zy, 03/15/11
        """
        mjd = self.std2mjd(str(std))
        return self.mjd2dyr(mjd)

    def dyr2std(self,dyr):
        """Converting from decimal year to STring Date.
        String date is in the form "%y%b%d"
        zy, 02/27/12
        """
        dyr = round(dyr,4)
        mjd = self.dyr2mjd(float(dyr))
        return self.mjd2std(mjd)

    def asmjd(self,t):
        """Converting everything to mjd.
"""
        if isinstance(t,float):
            return self.dyr2mjd(t)
        if isinstance(t,str):
            return self.std2mjd(t)
        if isinstance(t,int):
            return t
        msg = "The type of input parameter is wrong. Required type of t is "+\
              "either float or string or integer. But the actual type is "+\
              str(type(t))+"."
        raise ValueError(msg)

    def asdyr(self,t):
        """Converting everything to mjd.
"""
        if isinstance(t,float):
            return t
        if isinstance(t,str):
            return self.std2dyr(t)
        if isinstance(t,int):
            return self.mjd2dyr(t)
        msg = "The type of input parameter is wrong. Required type of t is "+\
              "either float or string or integer. But the actual type is "+\
              str(type(t))+"."
        raise ValueError(msg)

    def asstd(self,t):
        """Converting everything to std.
"""
        if isinstance(t,float):
            return self.dyr2std(t)
        if isinstance(t,str):
            return t
        if isinstance(t,int):
            return self.mjd2std(t)
        msg = "The type of input parameter is wrong. Required type of t is "+\
              "either float or string or integer. But the actual type is "+\
              str(type(t))+"."
        raise ValueError(msg)

# a global object used in this module.
date = Date()

def asmjd(t):
    """Converting everything to mjd.
"""
    global date
    if isinstance(t,list) or isinstance(t,tuple) or isinstance(t,ndarray):
        return asarray([date.asmjd(ii) for ii in t],dtype='int')
    return date.asmjd(t)
        
def asdyr(t):
    """Converting everything to dyr.
"""
    global date
    if isinstance(t,list) or isinstance(t,tuple) or isinstance(t,ndarray):
        return asarray([date.asdyr(ii) for ii in t],dtype='float')
    return date.asdyr(t)

def asstd(t):
    """Converting everything to std.
"""
    global date
    if isinstance(t,list) or isinstance(t,tuple) or isinstance(t,ndarray):
        return asarray([date.asstd(ii) for ii in t],dtype='str')
    return date.asstd(t)

def asdtype(t,dtype):
    """ Convert t to date type as indicated by dtype
"""
    global date
    if dtype=='mjd':
        return asmjd(t)
    if dtype=='dyr':
        return asdyr(t)
    if dtype=='std':
        return asstd(t)

    raise ValueError("Wrong date type.")

# testing
if __name__ == "__main__":
    print(date.mjd2dyr('55631'))
    print(date.dyr2mjd(2014.1896))

    



