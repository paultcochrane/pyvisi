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
This is the file for the Renderer class
"""

# generic imports
from pyvisi.renderers.povray.common import debugMsg
from pyvisi.renderer import Renderer as BaseRenderer

__revision__ = '$Revision$'

class Renderer(BaseRenderer):
    """
    A generic object holding a renderer of a Scene().
    """

    def __init__(self):
        """
        Initialisation of Renderer() class
        """
        debugMsg("Called Renderer.__init__()")
        BaseRenderer.__init__()

        # initialise some attributes
        self.renderWindowWidth = 640
        self.renderWindowHeight = 480

        # initialise the evalstack
        self._evalStack = ""

        # initialise the renderer module

        self.addToEvalStack("# Renderer.__init__\n")
        self.addToEvalStack("import gnuplot\n")

    def setRenderWindowWidth(self, width):
        """
        Sets the render window width
        
        @param width: The width of the render window
        @type width: float
        """
        self.renderWindowWidth = width
        return

    def setRenderWindowHeight(self, height):
        """
        Sets the render window height

        @param height: The height of the render window
        @type height: float
        """
        self.renderWindowHeight = height
        return

    def getRenderWindowWidth(self):
        """
        Gets the render window width
        """
        return self.renderWindowWidth

    def getRenderWindowHeight(self):
        """
        Gets the render window height
        """
        return self.renderWindowHeight

    def getEvalStack(self):
        """
        Gets the evaluation stack as it currently stands
        """
        return self._evalStack

    def addToEvalStack(self, evalString):
        """
        Method to add commands to the evaluation stack
        
        @param evalString: The string of commands to be added to the evalStack
        @type evalString: string
        """
        debugMsg("Called Renderer.addToEvalStack()")
        self._evalStack += evalString
        return

    def resetEvalStack(self):
        """
        Reset/flush the evaluation stack
        """
        debugMsg("Called Renderer.resetEvalStack()")
        self._evalStack = ""
        return

# vim: expandtab shiftwidth=4:
