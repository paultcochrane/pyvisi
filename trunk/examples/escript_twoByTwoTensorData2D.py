#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

tensorDomain = bruce.Rectangle(9,9,10,10)
tensorFunctionSpace=escript.ContinuousFunction(tensorDomain)

tensorData2x2 = numarray.array([[1.0,2.0],[3.0,4.0]])

# plotting 2x2 tensors in a 2D array
twoByTwoTensorData2D = Data(tensorData2x2, tensorFunctionSpace, True)
scene = Scene()
plot = EllipsoidPlot(scene)
plot.setData(twoByTwoTensorData2D)
scene.render(pause=True)

# vim: expandtab shiftwidth=4:
