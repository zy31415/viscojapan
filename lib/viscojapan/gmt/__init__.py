from .applications import *
from .gadgets import *

__doc__=''' I build three layers of code to wrap around GMT command
for the sake of my project.

* First Layer: command wrapper (pGMT package)
This is the original command wrapper layer.


* Second Layer: The "gadgets" package
Combination of several GMT commands to acoomplish a certain plot
task, for example, plot focal mechanisms,
plot slabs, etc. None of these gadgets can work independently.

* Third Layer: The "applications" package
Complete GMT commands that can draw a full plot. They output
a complete pdf file.

zy
Dec 5, 2014
'''
