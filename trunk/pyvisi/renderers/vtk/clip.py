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

"""
Class and functions associated with a pyvisi Clip* objects
"""

# generic imports
from pyvisi.renderers.vtk.common import debugMsg
from pyvisi.renderers.vtk.item import Item

__revision__ = '$Revision$'

class ClipPlane(Item):
    """
    Clip plane class: used to clip data sets with a plane
    """
    def __init__(self, scene):
        """
        Initialisation of the ClipPlane object

        @param scene: The Scene object to add the ClipPlane object to
        @type scene: Scene object
        """
        debugMsg("Called ClipPlane.__init__()")
        Item.__init__(self)

        self.renderer.addToEvalStack("# ClipPlane.__init__()")

        # keep a reference to the renderer so we can send stuff to it
        self.renderer = scene.renderer

        # set the default origin
        self.origin = (0.0, 0.0, 0.0)

        # set the default normal
        self.normal = (0.0, 1.0, 0.0)

        # set the default inside out flag value
        self.insideOut = False

    def setOrigin(self, x, y, z):
        """
        Set the origin of the plane
        """
        self.origin = (x, y, z)
        return

    def getOrigin(self):
        """
        Get the current origin of the plane
        """
        return self.origin

    def setNormal(self, vx, vy, vz):
        """
        Set the normal vector to the plane
        """
        self.normal = (vx, vy, vz)
        return

    def getNormal(self):
        """
        Get the current normal vector to the plane
        """
        return self.normal

    def setInsideOut(self, insideOut):
        """
        Set the inside out flag
        """
        self.insideOut = insideOut
        return

    def getInsideOut(self):
        """
        Get the current value of the inside out flag
        """
        return self.insideOut


class ClipBox(Item):
    """
    Clip box class: used to clip data sets with a box

    A box in this sense means three planes at right angles to one another
    """
    def __init__(self, scene):
        """
        Initialisation of the ClipBox object

        @param scene: The Scene object to add the ClipBox object to
        @type scene: Scene object
        """
        debugMsg("Called ClipBox.__init__()")
        Item.__init__(self)

        self.renderer.addToEvalStack("# ClipBox.__init__()")

        # keep a reference to the renderer so we can send stuff to it
        self.renderer = scene.renderer

        # set the default origin
        self.origin = (0.0, 0.0, 0.0)

        # set the default inside out flag value
        self.insideOut = False

    def setOrigin(self, x, y, z):
        """
        Set the origin of the plane
        """
        self.origin = (x, y, z)
        return

    def getOrigin(self):
        """
        Get the current origin of the plane
        """
        return self.origin

    def setInsideOut(self, insideOut):
        """
        Set the inside out flag
        """
        self.insideOut = insideOut
        return

    def getInsideOut(self):
        """
        Get the current value of the inside out flag
        """
        return self.insideOut

# vim: expandtab shiftwidth=4:
