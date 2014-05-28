This folder handles the job of computing greens functions.
Green's functions are computed with two software packages: STATIC1D and VISCO1D.
The final results are organized in a HDF5 file, which is usually called G.h5,
and served for inversion.

The folder comprises three modlues which are specified in the following:
(Please refer to a design flow chart in doc directory.)
Module One - earthmodel
=======================================================
Specific tasks:
(1) Generate earthmodel file for STATIC1D and VISCO1D
(2) Set up to run the earth model part of STATIC1D and VISCO1D.
(3) Provide interface for observation generation part of STATIC1D and VISCO1D
to access earth model results.
(4) Provide visualizetion toolkit for earthmodel file. 
They are crutial to results analysis.

Module Two - faultmodel
========================================================
(1) Generate fault models. Allow flexibility to adjust important parameters.
For example, elastic depth, fault and subfault dimentsion.
(2) Generate fault models input files for STATIC1D and VISCO1D.
Provide interface to access these files.
(3) Provide interface to access fault geometry.
(4) Provide visualization toolkit.

Module Three - greensfunction
========================================================
(1) Run observation generation part of STATIC1D and VISCO1D.
(2) Synthesize G matirx for inversion
(3) Do time interpolation and provide utilities to access G data
(4) Generate dG matrix based G matrix
(5) Freedom to choose which stations to include or not
(6) Virsulization tools for analysis

Other directories in this package:
(1) lib - library directory, python library greens is in it.
(2) doc - documentation

zy
May 28, 2014
