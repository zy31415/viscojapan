import argparse

import numpy as np
from scipy.interpolate import griddata
from pylab import plt

import viscojapan as vj

from utils import load_array
from epochs_log import epochs

parser = argparse.ArgumentParser(description='Plot percentage spatial.')
parser.add_argument('file', nargs='?', help='input file')
parser.add_argument('-ncmpt', nargs=1, type=int, help='cmoponent number')
parser.add_argument('-nepoch', nargs=1, type=int, help='epoch number')

parser.add_argument('-p', action='store_true', help='If show the plot.')
parser.add_argument('-o', nargs='*', default=False, help='Output a file.')

args = parser.parse_args()

fn = args.file
percentage = load_array(fn)

ncmpt = args.ncmpt[0]
nepoch = args.nepoch[0]

region_box = [130, 31, 143, 43]

tp = np.loadtxt(fn,'4a,')
sites = sorted(list(set([ii[0] for ii in tp])))
lons, lats = vj.get_pos(sites)

xi = np.linspace(region_box[0],region_box[2],100)
yi = np.linspace(region_box[1],region_box[3],100)
zi = griddata((lons, lats), percentage[ncmpt::3,nepoch], (xi[None,:], yi[:,None]),
              method='linear')

cmap = plt.cm.jet
cmap.set_bad('w',1.)

bm = vj.MyBasemap(region_box = region_box)
zi = np.ma.array(zi, mask=np.isnan(zi)) 
bm.pcolor(xi, yi, zi, latlon=True, cmap=cmap,zorder=-2)
bm.drawlsmask(land_color=(0,0,0,0),ocean_color='w',lakes=True, zorder=-2)
plt.colorbar()
plt.clim([0,1])
plt.title('Epoch = %d'%epochs[nepoch+1])

if args.p:
    plt.show()

if args.o:
    for file in args.o:
        plt.savefig(file)

plt.close()


