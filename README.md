PyVisi
======
  

--------------------------------------------------------------------
Summary
--------------------------------------------------------------------

PyVisi is the Python visualisation interface: a generic Python-based
interface to many different scientific visualisation packages.

--------------------------------------------------------------------
Installation
--------------------------------------------------------------------

PyVisi is just a python module ... treat it as any other module

### Global Installation

As root use

    $ python setup.py install

This will install the files, in the appropriate place for your python
distribution. This will be something like e.g.
`/usr/lib/python2.x/site-packages/`

### Local installation

You can supply the base directory using

    $ python setup.py install --home=<dir>

which will install the files in 

    <dir>/lib/python/

for more help and options use 

    $ python setup.py install --help

also see <http://www.python.org/doc/current/inst/> for more details on using
the distutils package.


--------------------------------------------------------------------
 Dependencies
--------------------------------------------------------------------

### Numerical backend packages

#### Numeric package

PyVisi does some computation, and to be able to do this requires the Numeric
python package.  You can get this from
<http://sourceforge.net/projects/numpy>

#### numarray package

For compatiblity with the escript package, PyVisi now depends upon the
numarray package as well as the Numeric package for some computations.  You
can get numarray from
<http://www.stsci.edu/resources/software_hardware/numarray>

### Renderer modules

PyVisi depends upon the relevant renderer module's application and/or python
wrappers to be installed so that the renderer module can be used.  At
present, the vtk and gnuplot renderer modules are being developed.

#### Gnuplot renderer module

You must have gnuplot installed (version 4.0 or above).  You can get gnuplot
from <http://www.gnuplot.info>.  Note that gnuplot version 3 is no longer
supported by pyvisi.

You must have the Gnuplot.py (version 1.7 or greater) python wrapper for
gnuplot.  You can get this from <http://gnuplot-py.sourceforge.net/>.

#### VTK renderer module

You must have vtk version 4.2 or above installed.  You can get vtk from
<http://www.vtk.org>.  Note that when you install vtk, that you must install
the python wrappers as well (this is explained in the vtk installation
information.)
