#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

brickDomain = bruce.Brick(9,9,9,10,10,10)
brickFunctionSpace=escript.ContinuousFunction(brickDomain)

vectorData2D = numarray.array([1.0,2.0])

# plotting 2D vectors in a 3D array
twoDVectorData3D = Data(vectorData2D, brickFunctionSpace, True)
scene = Scene()
plot = ArrowPlot3D(scene)
plot.setData(twoDVectorData3D)
scene.render()

# vim: expandtab shiftwidth=4:
