# Copyright (C) 2004 Paul Cochrane
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

# $Id$

## @file basicContourExample.py

"""
Example of a basic contour plot

Will hopefully help me write a decent interface.
"""

import sys,os

# this means that one can run the script from the examples directory
sys.path.append('../')

# import the python visualisation interface
from pyvisi import *

# original vtk code
import vtk

import numarray

# generate the x and y grid data
x = numarray.arrayrange(-2, 2, stride=0.1, type='Float')
y = numarray.arrayrange(-3, 3, stride=0.1, type='Float')

# generate a matrix of repeated x values (c.f. repmat() in matlab)
xm = numarray.zeros([len(x), len(y)], type='Float')
for i in range(len(y)):
    xm[:,i] = x

# generate a matrix of repeated y values (c.f. repmat() in matlab)
ym = numarray.zeros([len(x), len(y)], type='Float')
for i in range(len(x)):
    ym[i,:] = y

sigma = 0.2  # the spread of the distribution

# generate the distribution
distn = numarray.exp(-(xm*xm + ym*ym)/sigma)

xvtk = vtk.vtkFloatArray()
for i in range(len(x)):
    xvtk.InsertNextValue(x[i])

yvtk = vtk.vtkFloatArray()
for i in range(len(y)):
    yvtk.InsertNextValue(y[i])

distnvtk = vtk.vtkFloatArray()
for i in range(len(x)):
    for j in range(len(y)):
	distnvtk.InsertNextValue(distn[i,j])

grid = vtk.vtkStructuredGrid()
grid.SetDimensions((len(x), len(y), 1))
grid.SetPoints(points)
#rgrid.SetXCoordinates(xvtk)
#rgrid.SetYCoordinates(yvtk)

#dataArray = vtk.vtkDoubleArray()
#dataArray.SetNumberOfComponents(2)
#dataArray.SetNumberOfTuples(len(x)*len(y))
#for i in range(len(y)):
#    dataArray.SetTuple2(0,distn[:,i])

plane = vtk.vtkStructuredGridGeometryFilter()
plane.SetInput(grid)
#plane.SetExtent((0,40, 0,60, 0,0))

cont = vtk.vtkContourFilter()
cont.SetInput(plane.GetOutput())
cont.GenerateValues(10,0.0,1.0)

contMap = vtk.vtkPolyDataMapper()
contMap.SetInput(cont.GetOutput())
contMap.SetScalarRange(0.0,1.0)

contAct = vtk.vtkActor()
contAct.SetMapper(contMap)

planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInput(plane.GetOutput())

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
#planeActor.GetProperty().SetRepresentationToWireframe()
#planeActor.GetProperty().SetColor(0,0,0)

quadric = vtk.vtkQuadric()
quadric.SetCoefficients(0.5, 1, 0.2 ,0 ,0.1 ,0 ,0, 0.2, 0, 0)

sample = vtk.vtkSampleFunction()
sample.SetSampleDimensions(30,30,30)
sample.SetImplicitFunction(quadric)
sample.ComputeNormalsOff()

extract = vtk.vtkExtractVOI()
extract.SetInput(sample.GetOutput())
extract.SetVOI(0, 29, 0, 29, 15, 15)
extract.SetSampleRate(1, 2, 3)

contours = vtk.vtkContourFilter()
contours.SetInput(extract.GetOutput())
contours.GenerateValues(13, 0.0, 1.2)

contMapper = vtk.vtkPolyDataMapper()
contMapper.SetInput(contours.GetOutput())
contMapper.SetScalarRange(0.0, 1.2)

contActor = vtk.vtkActor()
contActor.SetMapper(contMapper)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

#ren.AddActor(contActor)
#ren.AddActor(planeActor)
ren.AddActor(contAct)
renWin.SetSize(400,400)
ren.SetBackground(0.1,0.2,0.4)
renWin.Render()
iren.Start()
#raw_input("Press enter to continue")


