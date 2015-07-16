#	VISCOJAPAN

	Deformation Analysis and Modeling for the 2011 Tohoku-Oki Earthquake


##	Introduction

	On March 11th, 2011, a giant megathrust happened off the Pacific coast of 
	Tohoku, Japan. This earthquake was the most powerful earthquake ever recorded to 
	have hit Japan and causes extensive co- and post-seismic deformation, which
	is recorded by more than one thousands GPS stations in and around Japan.

	This software package is designed for the analyze of GPS time series that are related with
	this earthquake and do the linear and non-linear modeling to infer earthquake 
	parameters and the rheological parameters of the Earth.

##	Languages used

* Python3 : Python is the main language used to write this package.
* R	 	  : R is integrated with Python to do linear regression analysis of 
				GPS time series.
* C/C++   : Some parts of Python are written with C/C++ to enhance 
				performance.

## Third-party Python libraries required
	* numpy : for scientific computation
	* scipy : for scientific computation
	* matplotlib : for 2D plotting
	* basemap : for 2D geographic plotting
	* rpy2 : R python wrapper
	* h5py : For results storage and efficient large data accessing
	* cvxopt : Python library for convex optimization
	* pyproj : Performs cartographic transformations and geodetic computations
	* simplekml : generate kml (or kmz) for displaying data on google map/earth
	

##	Author

	Yang Zhang (zy31415@gmail.com)
	University of Nevada, Reno
