# Copyright (C) 2004-2005 Paul Cochrane
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

## @file render.py

"""
This is the file for the vtk Renderer class
"""

# generic imports
from pyvisi.renderers.vtk.common \
        import debugMsg, getRevision
from pyvisi.renderer import Renderer as BaseRenderer

__revision__ = getRevision()

class Renderer(BaseRenderer):
    """
    A generic object holding a renderer of a Scene().
    """

    def __init__(self):
        """
        Initialisation of Renderer() class
        """
        BaseRenderer.__init__(self)
        debugMsg("Called Renderer.__init__()")

        # initialise some attributes
        self.renderWindowWidth = 640
        self.renderWindowHeight = 480

        # initialise the evalstack
        self._evalStack = ""

        # initialise the renderer module
        self.addToEvalStack("# Renderer._initRendererModule")
        self.addToEvalStack("import vtk")
        self.addToEvalStack("_renderer = vtk.vtkRenderer()")
        # this next line should only be done if we have an active display
        self.addToEvalStack("_renderWindow = vtk.vtkRenderWindow()")
        self.addToEvalStack("_renderWindow.AddRenderer(_renderer)")
        evalString = "_renderWindow.SetSize(%d,%d)" % \
                (self.renderWindowWidth,self.renderWindowHeight)
        self.addToEvalStack(evalString)

# vim: expandtab shiftwidth=4:
