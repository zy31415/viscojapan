from numpy import array

__doc__ = \
"""
This module defines the Data() class, which is used to contain data used in regression.
"""

__all__ = ['Data']

class Data():
    """ Data class is designed to store and manipulate data used in regression.
Data (t, y0, y0_sd) are stored in two ways,
because sometime we want to use only part of the data to do regression.
(_t, _y0, _y0_sd) are the actual time series used in regression.
"""
    def __init__(self):
        self.t = None
        self._t = None
        self.y0 = None
        self._y0 = None
        self.y0_sd = None
        self._y0_sd = None

    def set_t(self,t):
        """ Set t.
"""
        self.t = t;
        self._t = t;

    def set_y0(self,y0):
        """ Set y0.
"""
        self.y0 = y0
        self._y0 = y0

    def set_y0_sd(self,y0_sd):
        """ Set y0_sd.
"""
        self.y0_sd = y0_sd
        self._y0_sd = y0_sd

    def set_data(self, xxx_todo_changeme):
        """ Set t, y0, y0_sd togeter.
"""
        (t,y0,y0_sd) = xxx_todo_changeme
        if not (len(t)==len(y0) and len(t)==len(y0_sd)):
            raise ValueError('Data should have the same length.')
        for func, data in zip((self.set_t,self.set_y0,self.set_y0_sd,),
                              (t,y0,y0_sd)):
            func(data)

    def cut(self,tcuts):
        """ Cutting data. Time series data (t, y0, y0_sd) are stored in two ways,
because sometime we want to use only part of the data to do regression.
(_t, _y0, _y0_sd) are the actual time series used in regression.
"""
        ch = array([False]*len(self.t))
        for tcut in tcuts:
            t1 = tcut[0]
            t2 = tcut[1]
            ch = ch|(self.t>=t1)&(self.t<=t2)
        self._t = self.t[ch]
        self._y0 = self.y0[ch]
        self._y0_sd = self.y0_sd[ch]


    def __len__(self):
        """ Return the number of data points.
"""
        res = len(self._t)
        assert (res == len(self._y0) and res == len(self._y0_sd))
        return res
        
