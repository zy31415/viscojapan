This folder handles the job of computing greens functions.
Green's functions are computed with two software packages: STATIC1D and VISCO1D.
The final results are organized in a HDF5 file, which is usually called G.h5.

The following are detailed analysis of task of this folder:

Part One - Model Geometry - Earth Model and Fault Model
=======================================================
Specific tasks:
(1) Decide proper gemetric model for earth and fault.
For example, elastic depth, subfaults dimensions, etc.

(2) Provide inputs for STATIC1D and VISCO1D.
(3) Provide proper interfaces to access geometry of earth and fault model
(4) Provide visualizetion toolkit for earth and fault models. 
They are crutial to results analysis.


Part Two - STATIC1D and VISCO1D
========================================================
There are two steps for computing deformation observations using these two packages:

(1) Resolve earth model

(2) Compute Observations 

The execution of these two routines should be wrapped under python.

Part Three - Synthesize final results
========================================================
(1) Form epochal G matrix data.
(2) Provide utilities to access G data
(3) Do interpolation
(4) Freedom to choose which stations to include or not
(5) Virsulization tools for analysis


zy
May 28, 2014
