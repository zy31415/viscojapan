#!/bin/bash
gmt psbasemap -R128/148/30/46 -U20/0/25/Yang -B4 -P -K -JB138/38/30/46/16c > out.ps
gmt grdimage ~tmp/grd -R -J -Q -K -C~tmp/cpt -O > out.ps
gmt pscoast -Swhite -R -J -K -O > out.ps
gmt psscale -O -D4/9/4/.2 -B1::/:m: -Q -K -C~tmp/cpt > out.ps
gmt grdcontour ~tmp/grd -R -C/tmp/tmpj7ccfbxw -J -A1+f9+um -K -Wthick -O -Gn1/.5c > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -R -O -J -K -Wthick,150 -Sf0.25/3p -G150 > out.ps
gmt pscoast -R -Dh -J -K -Wfaint,100 -O -Na/faint,50,-- -Lf145/31/38/200+lkm+jt > out.ps
gmt psmeca /tmp/tmpuzf2vfxd -R -J -Sc0.400000 -O -h1 > out.ps
