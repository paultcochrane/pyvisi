#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

brickDomain = bruce.Brick(9,9,9,10,10,10)
brickFunctionSpace=escript.ContinuousFunction(brickDomain)

vectorData3D = numarray.array([1.0,2.0,3.0])

# plotting 3D vectors in a 3D array
threeDVectorData3D = Data(vectorData3D, brickFunctionSpace, True)
scene = Scene()
plot = ArrowPlot3D(scene)
plot.setData(threeDVectorData3D)
scene.render(pause=True)

# vim: expandtab shiftwidth=4:
