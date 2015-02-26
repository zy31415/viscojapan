Run3
The old regularization method:
1. Coseismic slip - 2nd order
2. Afterslip - 0th order

Aterslip need to be smooth, too.
Change to the following regularization method:
2nd order for all
and 0zth order for afterslip.

Use BasisMatrixBSpline as basis function.


Run7
Use unit matrix for basis matrix.
I didn't handle basis matrix carefully, thus causes a lot trouble.
Jan 05, 2015

=====
Run8
(1) Evenly space the time. 
(2) According to euler's performance, I use more epochs.

Feb 16, 2015

=====
Run9
Add a new constraint: slip rate must be decreasing.

Feb 16, 2015

=====
Run10
Change the SD of coseismic displacement to 0.5.

Feb 25, 2015
