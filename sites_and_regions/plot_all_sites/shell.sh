#!/bin/bash
gmt psbasemap -R95/160/12/55 -K -B10g10 -JB127.5/33.5/12/55/19c -U18/25/0 > out.ps
gmt grdimage topo.grd -J -O -Itopo_grad.grd -K -Cafrikakarte.cpt > out.ps
gmt pscoast -O -Wfaint,50 -K -Na/faint,100,-. -R -Dl -J -Lf155/15/35/500+lkm+jt -A1000 > out.ps
gmt psxy /home/zy/workspace/viscojapan/share/plate_boundary_PB/PB2002_boundaries.gmt -O -R -G100 -Wthick,100 -J -Sf0.25/3p -K > out.ps
gmt psmeca /tmp/tmp7_vweyvi -O -J -h1 -R -K -Sc0.200000 > out.ps
gmt psxy japan.gmt -O -R -Gbrown -Wfaint,brown -J -K -Sc0.04 > out.ps
gmt psxy korea.gmt -O -R -Gblue -Wfaint,blue -J -K -St0.09 > out.ps
gmt psxy china.gmt -O -R -Gdarkgreen -Wfaint,darkgreen -J -K -Sa0.2 > out.ps
gmt psxy igs.gmt -O -R -Gred -Wfaint,red -J -K -Sd0.12 > out.ps
gmt pslegend /tmp/tmp0fti7w96 -O -R -L1.2 -F+gazure1 -J -D144/33/3.2/1.5/BL -C0.04i/0.07i > out.ps
