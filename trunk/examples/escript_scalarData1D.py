#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

vectorDomain = bruce.Rectangle(9,1,10,1)
vectorFunctionSpace=escript.ContinuousFunction(vectorDomain)

scalarData = 1.0


# plotting scalar data in a 1D array
scalarData1D = Data(scalarData, vectorFunctionSpace, True)
scene = Scene()
plot = LinePlot(scene)
plot.setData(scalarData1D)
scene.render(pause=True)
# what other kinds of plot should I use for this kind of data??

# vim: expandtab shiftwidth=4:
