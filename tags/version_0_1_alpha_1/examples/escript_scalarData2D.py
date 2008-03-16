#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

tensorDomain = bruce.Rectangle(9,9,10,10)
tensorFunctionSpace=escript.ContinuousFunction(tensorDomain)
domainData = tensorFunctionSpace.getX()

# plotting scalar data in a 2D array
scalarData2D = sin(domainData[0])

scene = Scene()
plot = ContourPlot(scene)
plot.setData(scalarData2D)
scene.render(pause=True)

scene.save(fname="escript_scalarData2D_contourPlot.png", format="png")

scene = Scene()
plot = SurfacePlot(scene)
plot.setData(scalarData2D)
scene.render(pause=True)

scene.save(fname="escript_scalarData2D_surfacePlot.png", format="png")

# add SurfacePlot, MeshPlot etc here

# vim: expandtab shiftwidth=4: