#!/bin/bash
gmt psbasemap -K -JB138/38/30/46/16c -U20/0/25/Yang -P -R128/148/30/46 -B4 > out.ps
gmt grdimage ~tmp/grd -K -J -C~tmp/cpt -Q -O -R > out.ps
gmt pscoast -K -J -Swhite -R -O > out.ps
gmt psscale -K -D4/9/4/.2 -C~tmp/cpt -Q -O -B1::/:m: > out.ps
gmt grdcontour ~tmp/grd -K -J -Gn1/.5c -A1+f9+um -C/tmp/tmpqux_dhue -Wthick -O -R > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -K -J -G150 -Wthick,150 -Sf0.25/3p -O -R > out.ps
gmt pscoast -Lf145/31/38/200+lkm+jt -J -K -Dh -Wfaint,100 -O -R -Na/faint,50,-- > out.ps
gmt psmeca /tmp/tmp_7nwyviy -J -O -Sc0.400000 -R -h1 > out.ps
