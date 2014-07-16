import glob

from pylab import *
from numpy.linalg import norm
import h5py

from viscojapan.epochal_data import vstack_column_vec, EpochalSlip

from alphas import alphas
from betas import betas
from epochs_even import epochs

ep = EpochalSlip('../../gaussian_slip.h5')
m_true = vstack_column_vec(ep, epochs)

x = alphas
y = betas
xx,yy = meshgrid(x,y)

zz = xx*0.

for ano, alpha in enumerate(alphas):
    for bno, beta in enumerate(betas):
        with h5py.File('../../outs_alpha_beta/res_a%02d_b%02d.h5'%(ano,bno),'r') as fid:
            m = fid['m'][...]
        zz[ano, bno] = norm(m-m_true)
        
pcolor(xx,yy,zz, zorder=-1)

ano = 16
bno = 21
plot(alphas[ano], betas[bno], marker='o',ms=10, color='red')
xlabel('alpha')
xlabel('beta')

ax =  gca()
ax.set_yscale('log')
ax.set_xscale('log')

colorbar()
show()
    
