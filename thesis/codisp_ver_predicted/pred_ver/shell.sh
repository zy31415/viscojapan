#!/bin/bash
gmt psbasemap -K -P -U20/0/25/Yang -JB138/38/30/46/16c -R128/148/30/46 -B4 > out.ps
gmt grdimage ~tmp/grd -K -J -R -Q -O -Cvertical_disp.cpt > out.ps
gmt pscoast -Swhite -R -J -O -K > out.ps
gmt psscale -K -D4/9/4/.2 -O -B0.2::/:m: -Cvertical_disp.cpt > out.ps
gmt grdcontour ~tmp/grd -Gn1/.5c -K -A1+f9+um -Wthick -R -J -O -C/tmp/tmpgtzpyy0r > out.ps
gmt psxy /home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/PB2002_boundaries.gmt -K -Wthick,150 -Sf0.25/3p -O -J -R -G150 > out.ps
gmt pscoast -K -Wfaint,100 -Na/faint,50,-- -Dh -R -J -O -Lf145/31/38/200+lkm+jt > out.ps
gmt psmeca /tmp/tmp9f6rjcxo -h1 -Sc0.400000 -O -J -R > out.ps
