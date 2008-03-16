#!/usr/bin/env python


# $Id$

from esys.escript import *
from esys import bruce

import numarray

from pyvisi import *
from pyvisi.renderers.vtk import *

vectorDomain = bruce.Rectangle(9,1,10,1)
vectorFunctionSpace=escript.ContinuousFunction(vectorDomain)

vectorData2D = numarray.array([1.0,2.0])

# plotting 2D vectors in a 1D array
twoDVectorData1D = Data(vectorData2D, vectorFunctionSpace, True)

scene = Scene()
plot = ArrowPlot(scene)
plot.setData(twoDVectorData1D)
scene.render(pause=True)

scene.save(fname="escript_twoDVectorData1D_arrowPlot.png", format="png")

# vim: expandtab shiftwidth=4: