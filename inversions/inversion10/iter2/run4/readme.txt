The old regularization method:
1. Coseismic slip - 2nd order
2. Afterslip - 0th order

Aterslip need to be smooth, too.
Change to the following regularization method:
2nd order for all
and 0zth order for afterslip.

Use BasisMatrixBSpline as basis function.

====================
Run4:
Use regularization class:
ExpandForCumulativeSlip
to generate regularization.

use function:
create_CumuRough_Edge_Temp_regularization

i.e. regularize the roughening of the total slip, 
not the incremental slip.
Dec 18, 2014

