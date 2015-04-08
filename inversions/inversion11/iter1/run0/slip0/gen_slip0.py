import h5py
from pylab import plt

import viscojapan as vj

reader = vj.inv.ResultFileReader('nrough_05_naslip_11.h5')
slip = reader.get_slip()

slip.save('slip0.h5')
