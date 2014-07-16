''' This script devides the inverted moment into
equal sections to optimize the inversion.
'''
from numpy import asarray, rint
from scipy.interpolate import interp1d
from scipy.optimize import root

from viscojapan.plot_utils import Map, append_title
from viscojapan.fault.mo import get_mos_mws_from_epochal_file

from epochs_log import epochs

ano = 10
bno = 10
ep_slip = '../../outs_log/slip_a%02d_b%02d.h5'%(ano, bno)

mos, mws, epochs = get_mos_mws_from_epochal_file(ep_slip)

def integrate_Mo(t):
    mos_post = mos - mos[0]
    f = interp1d(epochs, mos_post, 'cubic')
    return f(t)

M_max = integrate_Mo(1100)

N_sections = 20

ti_int = []
for nth in range(1, N_sections):
    ro  = root(lambda t : integrate_Mo(t) - nth*M_max/N_sections, 1)
    ti = ro['x'][0]
    ti_int.append(rint(ti))
    print(ti, rint(ti), integrate_Mo(ti))

for ii in ti_int:
    print('%d, '%int(ii), end=""),
