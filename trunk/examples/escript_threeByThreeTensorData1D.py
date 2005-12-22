#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

vectorDomain = bruce.Rectangle(9,1,10,1)
vectorFunctionSpace=escript.ContinuousFunction(vectorDomain)

tensorData3x3 = numarray.array([[1.0,2.0,3.0],[3.0,4.0,5.0],[5.0,6.0,7.0]])

# plotting 3x3 tensors in a 1D array
threeByThreeTensorData1D = Data(tensorData3x3, vectorFunctionSpace, True)
scene = Scene()
plot = EllipsoidPlot(scene)
plot.setData(threeByThreeTensorData1D)
scene.render(pause=True)

# vim: expandtab shiftwidth=4:
