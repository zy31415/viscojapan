#!/bin/bash
gmt psbasemap -JB138/38/30/46/16c -R128/148/30/46 -K -B4:.Observed Magnitude of Horizontal Coseismic Disp: -U20/0/25/Yang -P > out.ps
gmt grdimage ~ver.grd -J -O -R -C~hor_mag.cpt -K > out.ps
gmt pscoast -O -J -Swhite -R -K > out.ps
gmt psxy /home/zy/workspace/viscojapan/share/plate_boundary_PB/PB2002_boundaries.gmt -Wthick,150 -Sf0.25/3p -J -R -K -G150 -O > out.ps
gmt pscoast -Wfaint,100 -J -R -O -Na/faint,50,-- -Dh -K -Lf145/31/38/200+lkm+jt > out.ps
gmt grdcontour ~ver.grd -J -A1+f8+um -R -O -Gn1/.5c -K -C/tmp/tmp43vf9ztx > out.ps
gmt psmeca /tmp/tmpltdqpfkc -J -Sc0.4 -R -O -K -h1 > out.ps
gmt psscale -Q -D4/9c/4c/.2c -Baf::/:m: -C~hor_mag.cpt -O > out.ps
