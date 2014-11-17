#!/bin/bash
gmt psbasemap -P -U20/0/22/Yang -R125/133/33/39 -JB129/36/33/39/15c -B2 -K > out.ps
gmt grdimage ~topo.grd -I~topo_grad.grd -J -O -C/home/zy/workspace/viscojapan/lib/viscojapan/gmt/share/afrikakarte.cpt -K > out.ps
gmt psvelo ../disp -R -O -W0.5,black -hi -K -Gblack -J -Sr30/1/0 -A0.07i/0.1i/0.1i+a45+g+e > out.ps
gmt psvelo /tmp/tmpwhf8kw_0 -R -O -W0.5,black -hi -K -Gblack -J -Sr30.000000/1/0 -A0.07i/0.1i/0.1i+a45+g+e+jc > out.ps
gmt pstext /tmp/tmpkdz6j3z8 -J -R -O -F+f8+jLB -K > out.ps
gmt psvelo baek_2012/baek_2012_obs -R -O -W0.5,red -hi -K -Gred -J -Sr30/1/0 -A0.07i/0.1i/0.1i+a45+g+e > out.ps
gmt psvelo /tmp/tmp7sw_rj3b -R -O -W0.5,red -hi -K -Gred -J -Sr30.000000/1/0 -A0.07i/0.1i/0.1i+a45+g+e+jc > out.ps
gmt pstext /tmp/tmpilvyxcf1 -J -R -O -F+f8+jLB -K > out.ps
gmt pscoast -Lf144/35.4/38/100+lkm+jt -Dh -O -Wfaint,100 -J -Na/faint,50,-- -R -K -A500 > out.ps
gmt psmeca /tmp/tmpyu84qyu6 -Sc0.400000 -R -O -h1 -J > out.ps
