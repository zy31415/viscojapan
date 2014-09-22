This package is a python wrapper for DC3D fortran package (Okada model).
The source of this package can be downloaded at:
http://www.bosai.go.jp/study/application/dc3d/DC3Dhtml_E.html

The original source file DC3D.f was modified by changing data type real*4 into real*8.

Then the following command was used to generate the signature file:

f2py3.2 DC3D.f -m _DC3D -h dc3d.pyf

Then the generated signature file dc3d.pyf was edited by adding parameters to indicate outputs, 
for example change:
real*8 :: ux
into:
real*8 intent(out):: ux

Finally use the following command to generate the module (in complile file):
f2py3.2 -c dc3d.pyf DC3D.f

-Yang
Mar 11, 2014
