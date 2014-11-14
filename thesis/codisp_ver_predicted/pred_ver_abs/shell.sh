#!/bin/bash
gmt psbasemap -U20/0/25/Yang -JB138/38/30/46/16c -P -K -R128/148/30/46 -B4 > out.ps
gmt grdimage ~tmp/grd -J -K -R -O -C~tmp/cpt -Q > out.ps
gmt pscoast -K -Swhite -R -J -O > out.ps
gmt psscale -K -O -C~tmp/cpt -Q -D4/9/4/.2 -B1::/:m: > out.ps
gmt grdcontour ~tmp/grd -R -A1+f9+um -J -C/tmp/tmp1ah91vp2 -K -Wthick -O -Gn1/.5c > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -Sf0.25/3p -J -K -Wthick,150 -G150 -O -R > out.ps
gmt pscoast -J -Lf145/31/38/200+lkm+jt -K -Na/faint,50,-- -R -Dh -O -Wfaint,100 > out.ps
gmt psmeca /tmp/tmpuszefagl -J -h1 -Sc0.400000 -R -O > out.ps
