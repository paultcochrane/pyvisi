#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

tensorDomain = bruce.Rectangle(9,9,10,10)
tensorFunctionSpace=escript.ContinuousFunction(tensorDomain)

vectorData2D = numarray.array([1.0,2.0])

# plotting 2D vectors in a 2D array
twoDVectorData2D = Data(vectorData2D, tensorFunctionSpace, True)
scene = Scene()
plot = ArrowPlot(scene)
plot.setData(twoDVectorData2D)
scene.render()

# vim: expandtab shiftwidth=4:
