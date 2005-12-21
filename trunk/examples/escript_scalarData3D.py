#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

brickDomain = bruce.Brick(9,9,9,10,10,10)
brickFunctionSpace=escript.ContinuousFunction(brickDomain)

scalarData = 1.0

# plotting scalar data in a 3D array
scalarData3D = Data(scalarData, brickFunctionSpace, True)
scene = Scene()
plot = IsosurfacePlot(scene)
plot.setData(scalarData3D)
scene.render()

# vim: expandtab shiftwidth=4:
