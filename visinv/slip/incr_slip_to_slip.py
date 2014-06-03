#!/usr/bin/env python3
import sys

sys.path.append('/home/zy/workspace/viscojapan/lib')
from viscojapan.slip import *

f_incr_slip = 'incr_slip.h5'
f_slip = 'slip.h5'

incr_slip_to_slip(f_incr_slip, f_slip)

slip_to_incr_slip(f_slip, 'incr_slip2.h5')
