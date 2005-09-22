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
The classes associated with Boxes
"""

# generic imports
from pyvisi.renderers.vtk.common import debugMsg

# module specific imports
from pyvisi.renderers.vtk.item import Item

__revision__ = '$Revision$'

class Box(Item):
    """
    Generic class for Box objects
    """

    def __init__(self, scene):
        """
        Initialisation of the Box object
        """
        debugMsg("Called Box.__init__()")
        Item.__init__(self)

        # define a box in many ways, either by its centre and width, height
        # and depth, or by its bounds, xmin, xmax, ymin, ymax, zmin, zmax,
        # or by its bottom left front and top right back points.

        # keep a reference to the renderer so we can send stuff to it
        self.renderer = scene.renderer

        # set the default origin
        self.origin = (0.0, 0.0, 0.0)

        # set the default dimensions
        self.width = 1.0
        self.height = 1.0
        self.depth = 1.0

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

    def render(self):
        """
        Perform Box object specific (pre)rendering tasks
        """
        debugMsg("Called Box.render()")


class ClipBox(Box):
    """
    Clip box class: used to clip data sets with a box

    A box in this sense means three planes at right angles to one another
    """

    def __init__(self):
        """
        Intialisation of the ClipBox object
        """
        debugMsg("Called ClipBox.__init__()")
        Box.__init__(self)

        # set the default inside out flag value
        self.insideOut = False

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
