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

## @file render.py

"""
This is the file for the Renderer class
"""

# generic imports
from common import _debug, rendererName
from pyvisi.renderer import Renderer as BaseRenderer

class Renderer(BaseRenderer):
    """
    A generic object holding a renderer of a Scene().
    """

    def __init__(self):
        """
        Initialisation of Renderer() class
        """
        if _debug: print "\t%s: Called Renderer.__init__()" % rendererName

        # initialise some attributes
        self.renderWindowWidth = 640
        self.renderWindowHeight = 480

        # initialise the evalstack
        self._evalStack = ""

        # initialise the renderer module

        self.addToEvalStack("# Renderer._initRendererModule\n")
        self.addToEvalStack("import vtk\n")
        self.addToEvalStack("_renderer = vtk.vtkRenderer()\n")
        # this next line should only be done if we have an active display
        self.addToEvalStack("_renderWindow = vtk.vtkRenderWindow()\n")
        self.addToEvalStack("_renderWindow.AddRenderer(_renderer)\n")
        evalString = "_renderWindow.SetSize(%d,%d)\n" % \
                (self.renderWindowWidth,self.renderWindowHeight)
        self.addToEvalStack(evalString)

        return

# vim: expandtab shiftwidth=4:
