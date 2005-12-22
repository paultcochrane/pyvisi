#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

tensorDomain = bruce.Rectangle(9,9,10,10)
tensorFunctionSpace=escript.ContinuousFunction(tensorDomain)

scalarData = 1.0

# plotting scalar data in a 2D array
scalarData2D = Data(scalarData, tensorFunctionSpace, True)
scene = Scene()
plot = ContourPlot(scene)
plot.setData(scalarData)
scene.render(pause=True)
# add SurfacePlot, MeshPlot etc here

# vim: expandtab shiftwidth=4:
