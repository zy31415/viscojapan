#	VISCOJAPAN

	Deformation Analysis and Modeling for the 2011 Tohoku-Oki Earthquake


##	Introduction

	On March 11th, 2011, a giant megathrust happened off the Pacific coast of 
	Tohoku, Japan. This earthquake was the most powerful earthquake ever recorded to 
	have hit Japan and causes extensive co- and post-seismic deformation, which
	is recorded by more than one thousands GPS stations in and around Japan.

	This software package is designed for the analyze of GPS time series that are related with
	this earthquake and do the linear and non-linear modeling to infer earthquake 
	parameters and the rheological parameters of the Earth. Specifically, this
	package contains the following parts:
		1) GPS time series management (sqlite3 database);  
		2) GPS time series modeling­ - Linear modeling of pre­seismic GPS time series;  
		3) GPS time series modeling - Nonlinear inversion of co­seismic slip and afterslip (solve for more than 10, 000 parameters);			
		4) Results analysis and report.  


## Package structure
	All libraries developed for the project can be found under lib/ directory.
	All the unit tests of these libraries are under test/.
	Other directories are for specific experiments or tasks.

## Libraries
	All libraries developed for this project can be found under lib/ directory.

### viscojapan : lib/viscojapan/­ 
	All the linear and nonlinear analysis are implemented in this library.
	
*	lib/viscojapan/tsana/	
	Linear analysis ­R wrapper for linear regression analysis.

*	lib/viscojapan/
	Nonlinear analysis – The core is the method of convex optimization 
	provided by an open source Python package called cvxopt. There are at
	least three layers are built upon this computational core to handle
	different situations of my projects.

### dpool : lib/dpool/ ­ 
	Multiprocessing with Python
	I designed and implemented a library called Dynamic POOL (dpool),
	where the number of running processes is dynamically managed so that
	when the system load from other users is heavy, the number of
	processes is reduced, and vice versus.

###	latex ­: lib/latex/
	A Python wrapper for Latex to combine subplots.

###	pGMT : lib/pGMT/
	A wrapper for GMT for geographic plotting.


##	Languages used

* 	Python3 : Python is the main language used to write this package.
* 	R	 	  : R is integrated with Python to do linear regression analysis of 
				GPS time series.
* 	C/C++   : Some parts of Python are written with C/C++ to enhance 
				performance.

## Third-party Python libraries used

* 	numpy : for scientific computation
* 	scipy : for scientific computation
* 	matplotlib : for 2D plotting
* 	basemap : for 2D geographic plotting
* 	rpy2 : R python wrapper
* 	h5py : For results storage and efficient large data accessing
* 	cvxopt : Python library for convex optimization
* 	pyproj : Performs cartographic transformations and geodetic computations
* 	simplekml : generate kml (or kmz) for displaying data on google map/earth	


##	Author

	For any questions, please contact the author:

	Yang Zhang (@zy31415)
	zy31415@gmail.com
	University of Nevada, Reno
