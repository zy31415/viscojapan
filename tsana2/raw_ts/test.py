#!/usr/bin/env python3
from pylab import *

_ts_data_type=dtype("a4,a7,f,i,i,i,3f,f,3f,f,f")

tp=loadtxt('IGS08/J550.IGS08.tenv',_ts_data_type)
