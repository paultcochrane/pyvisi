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

        # set the default bounds
        self.xmin = -0.5
        self.xmax = 0.5
        self.ymin = -0.5
        self.ymax = 0.5
        self.zmin = -0.5
        self.zmax = 0.5

        # set the default origin
        self.origin = ((self.xmin + self.xmax)/2.0, 
                (self.ymin + self.ymax)/2.0, 
                (self.zmin + self.zmax)/2.0)

        # set the default dimensions
        self.width = self.xmax - self.xmin
        self.height = self.ymax - self.ymin
        self.depth = self.zmax - self.zmin

        # set the default blf and trb points
        self.blf = (self.xmin, self.ymin, self.zmin)
        self.trb = (self.xmax, self.ymax, self.zmax)

    def setBounds(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """
        Set the bounds of the box
        """
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.zmin = zmin
        self.zmax = zmax
        return

    def getBounds(self):
        """
        Get the current bounds of the box
        """
        return (self.xmin, self.xmax, \
                self.ymin, self.ymax, \
                self.zmin, self.zmax)

    def setOrigin(self, xo, yo, zo):
        """
        Set the origin of the box
        """
        self.origin = (xo, yo, zo)
        return

    def getOrigin(self):
        """
        Get the current origin of the box
        """
        return self.origin

    def setWidth(self, width):
        """
        Set the width of the box
        """
        self.width = width
        return

    def getWidth(self):
        """
        Get the current box width
        """
        return self.width

    def setHeight(self, height):
        """
        Set the box height
        """
        self.height = height
        return

    def getHeight(self):
        """
        Get the current box height
        """
        return self.height

    def setDepth(self, depth):
        """
        Set the box depth
        """
        self.depth = depth
        return

    def getDepth(self):
        """
        Get the current box depth
        """
        return self.depth

    def setBLF(self, bottom, left, front):
        """
        Set the position of the bottom, left, front corner
        """
        self.blf = (bottom, left, front)
        return

    def getBLF(self):
        """
        Get the current position of the bottom, left, front corner
        """
        return self.blf

    def setTRB(self, top, right, back):
        """
        Set the position of the top, right, back corner
        """
        self.trb = (top, right, back)
        return

    def getTRB(self):
        """
        Get the current position of the top, right, back corner
        """
        return self.trb

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
