#!/bin/bash
gmt psbasemap -R138/145/35/42 -K -B2:.Oberved coseismic disp: -P -JB141.5/38.5/35/42/15c -U20/0/22/Yang > out.ps
gmt grdimage ~ver.grd -O -J -K -Cvertical_disp.cpt -R > out.ps
gmt pscoast -O -R -J -K -Swhite > out.ps
gmt psxy /home/zy/workspace/viscojapan/share/slab1.0/kur_top.in -O -J -Wthin, 50 -K -R > out.ps
gmt psxy ../../share/slab1.0/kur_contours_above_100km.in -J -R -O -Wthin, 50, -- -K -SqL144/41.5/138/41.5:+Lh+ukm > out.ps
gmt pscoast -K -Na/faint,50,-- -R -O -Dh -Wfaint,100 -Lf144/35.4/38/100+lkm+jt -J > out.ps
gmt psvelo /tmp/tmpr9oy9rws -J -hi -Sr0.6/1/0 -Gblack -A0.07i/0.1i/0.1i+a45+g+e -O -W0.5, black -K -R > out.ps
gmt psvelo /tmp/tmpsg7vw6yb -J -hi -Sr0.75/1/0 -Gblack -A0.07i/0.1i/0.1i+a45+g+e+jc -O -W0.5, black -K -R > out.ps
gmt pstext /tmp/tmp31qu4fg8 -O -J -K -F+f8+jLB -R > out.ps
gmt psmeca /tmp/tmp4t0fomco -J -h1 -K -O -R -Sc0.4 > out.ps
gmt psscale -O -D1.4/14c/4c/.2c -Baf::/:m: -Cvertical_disp.cpt > out.ps
