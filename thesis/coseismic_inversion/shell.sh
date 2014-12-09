#!/bin/bash
gmt psbasemap -P -R140/145/35/41.5 -B2 -JB142.5/38.5/35/41.5/14c -K -U18/25/0 > out.ps
gmt grdimage /tmp/tmpv6ki826b -J -K -I/tmp/tmp6v24mjbh -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -O > out.ps
gmt grdimage ~tmp/slip_cutted.grd -J -R -I~tmp/intensity.grd -O -G -K -C~tmp/slip.cpt -Q > out.ps
gmt grdcontour ~tmp/slip_cutted.grd -J -Gn1/.5c -A1+f9+um -O -R -Wthickest -K -C/tmp/tmppegggalq > out.ps
gmt pslegend /tmp/tmpalsqd4oc -J -R -F+gazure1 -L1.2 -O -K -D143.5/35.2/4/1.2/BL -C0.04i/0.07i > out.ps
gmt pslegend /tmp/tmp6mrg8ecm -J -R -F+gazure1 -L1.2 -O -K -D143.5/35.2/4/1.5/BL -C0.04i/0.07i > out.ps
gmt pscoast -J -R -L144.3/36/38/50+lkm+jt -A1000 -O -Wfaint,50 -K -Dh -Na/faint,150,-. > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -J -R -O -Gred -Wthick,red -K -Sf0.25/3p+r+b > out.ps
gmt psmeca /tmp/tmp0gltla6l -J -R -T -Lblack -O -Wblack -h0 -Sm0.400000/0.000000 > out.ps
