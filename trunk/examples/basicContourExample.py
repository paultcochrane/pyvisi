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
x = numarray.arrayrange(-1, 1, stride=0.5, type='Float')
y = numarray.arrayrange(-1, 1, stride=0.5, type='Float')

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

# convert the x data into vtkFloatArray objects
xvtk = vtk.vtkFloatArray()
for i in range(len(x)):
    xvtk.InsertNextValue(x[i])

# convert the y data into vtkFloatArray objects
yvtk = vtk.vtkFloatArray()
for i in range(len(y)):
    yvtk.InsertNextValue(y[i])

# convert the distribution data into vtkFloatArray objects
distnvtk = vtk.vtkFloatArray()
for i in range(len(x)):
    for j in range(len(y)):
        distnvtk.InsertNextValue(distn[i,j])

# make the points to put into the grid
points = vtk.vtkPoints()
values = vtk.vtkFloatArray()
count = 0
for i in xrange(len(x)):
    for j in xrange(len(y)):
        points.InsertPoint(count, x[i], y[j], 0)
        values.InsertValue(count, distn[i,j])
        count += 1

# now make the strips (whatever they are...)
strips = vtk.vtkCellArray()
strips.InsertNextCell(len(x)*len(y))  # number of points
for i in xrange(len(x)*len(y)):
    strips.InsertCellPoint(i)

#strips.InsertCellPoint(0)
#strips.InsertCellPoint(1)
#strips.InsertCellPoint(7)
#strips.InsertCellPoint(6)
#strips.InsertCellPoint(2)
#strips.InsertCellPoint(3)
#strips.InsertCellPoint(5)
#strips.InsertCellPoint(4)

# set up the polygonal data object
polyData = vtk.vtkPolyData()
polyData.SetPoints(points)
polyData.SetStrips(strips)
polyData.GetPointData().SetScalars(values)

warp = vtk.vtkWarpScalar()
warp.SetInput(polyData)
warp.SetScaleFactor(0.5)

contMapper = vtk.vtkPolyDataMapper()
contMapper.SetInput(warp.GetPolyDataOutput())
contMapper.SetScalarRange(polyData.GetScalarRange())

contActor = vtk.vtkActor()
contActor.SetMapper(contMapper)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(contActor)
renWin.SetSize(400,400)
ren.SetBackground(1,1,1)
iren.Initialize()
renWin.Render()
iren.Start()
#raw_input("Press enter to continue")


# vim: expandtab shiftwidth=4:
