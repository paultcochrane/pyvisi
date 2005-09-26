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

    To define a box one specify one of three groups of things:
      - The bounds of the box: xmin, xmax, ymin, ymax, zmin, zmax
      - The dimensions and origin: width, height, depth and origin
      - The bottom left front and top right back corners: blf, trb
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

        # set the default origin (the centre of the box)
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

        # tolerance for calculated variables checking purposes
        self.tolerance = 1e-8

    def setBounds(self, xmin, xmax, ymin, ymax, zmin, zmax):
        """
        Set the bounds of the box
        """
        debugMsg("Called Box.setBounds()")
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
        debugMsg("Called Box.getBounds()")
        return (self.xmin, self.xmax, \
                self.ymin, self.ymax, \
                self.zmin, self.zmax)

    def setOrigin(self, xo, yo, zo):
        """
        Set the origin of the box
        """
        debugMsg("Called Box.setOrigin()")
        # get the current origin
        (xi, yi, zi) = self.getOrigin()

        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # get the difference between the two origins
        (xd, yd, zd) = (xo-xi, yo-yi, zo-zi)

        # move the bounds accordingly
        self.setBounds(xmin+xd, xmax+xd, ymin+yd, ymax+yd, zmin+zd, zmax+zd)

        # the calculated origin should be the same as the one desired to be
        # set by the user
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()
        self.origin = ((xmin + xmax)/2.0,
                (ymin + ymax)/2.0,
                (zmin + zmax)/2.0)
        
        # do a check to see if calculated origin is close enough to that
        # desired by the user (to within the tolerance)
        if __debug__:
            (xi, yi, zi) = self.getOrigin()
            originDiff = (xo-xi, yo-yi, zo-zi)
            for i in range(3):
                assert abs(originDiff[i]) < self.tolerance, \
                        "Origin not set to within tolerance"

        return

    def getOrigin(self):
        """
        Get the current origin of the box
        """
        debugMsg("Called Box.getOrigin()")
        return self.origin

    def setWidth(self, width):
        """
        Set the width of the box
        """
        debugMsg("Called Box.setWidth()")
        # get the current width
        oldWidth = self.getWidth()

        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # add half the difference between the new width and the old width
        # to the xmin and xmax variables
        halfDiff = (width - oldWidth)/2.0

        xminNew = xmin - halfDiff
        xmaxNew = xmax + halfDiff

        # reset the bounds
        self.setBounds(xminNew, xmaxNew, ymin, ymax, zmin, zmax)

        # set the width
        self.width = xmaxNew - xminNew

        # do a check to make sure the calculated width is what was asked for
        if __debug__:
            newWidth = self.getWidth()
            assert abs(newWidth - width) < self.tolerance, \
                    "Width not set to within tolerance"

        return

    def getWidth(self):
        """
        Get the current box width
        """
        debugMsg("Called Box.getWidth()")
        return self.width

    def setHeight(self, height):
        """
        Set the box height
        """
        debugMsg("Called Box.setHeight()")
        # get the current height
        oldHeight = self.getHeight()

        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # add half the difference between the new height and the old height
        # to the ymin and ymax variables
        halfDiff = (height - oldHeight)/2.0

        yminNew = ymin - halfDiff
        ymaxNew = ymax + halfDiff

        # reset the bounds
        self.setBounds(xmin, xmax, yminNew, ymaxNew, zmin, zmax)

        # set the height
        self.height = ymaxNew - yminNew

        # do a check to make sure the calculated height is what was asked
        # for
        if __debug__:
            newHeight = self.getHeight()
            assert abs(newHeight - height) < self.tolerance, \
                    "Height not set to within tolerance"

        return

    def getHeight(self):
        """
        Get the current box height
        """
        debugMsg("Called Box.getHeight()")
        return self.height

    def setDepth(self, depth):
        """
        Set the box depth
        """
        debugMsg("Called Box.setDepth()")
        # get the current depth
        oldDepth = self.getDepth()

        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # add half the difference between the new depth and the old depth
        # to the zmin and zmax variables
        halfDiff = (depth - oldDepth)/2.0

        zminNew = zmin - halfDiff
        zmaxNew = zmax + halfDiff

        # reset the bounds
        self.setBounds(xmin, xmax, ymin, ymax, zminNew, zmaxNew)

        # set the depth
        self.depth = zmaxNew - zminNew

        # do a check to make sure the calculated depth is what was asked
        # for
        if __debug__:
            newDepth = self.getDepth()
            assert abs(newDepth - depth) < self.tolerance, \
                    "Depth not set to within tolerance"

        return

    def getDepth(self):
        """
        Get the current box depth
        """
        debugMsg("Called Box.getDepth()")
        return self.depth

    def setBLF(self, bottom, left, front):
        """
        Set the position of the bottom, left, front corner
        """
        debugMsg("Called Box.setBLF()")
        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # set the new bounds
        self.setBounds(bottom, xmax, left, ymax, front, zmax)

        # set the blf variable
        self.blf = (bottom, left, front)
        return

    def getBLF(self):
        """
        Get the current position of the bottom, left, front corner
        """
        debugMsg("Called Box.getBLF()")
        return self.blf

    def setTRB(self, top, right, back):
        """
        Set the position of the top, right, back corner
        """
        debugMsg("Called Box.setTRB()")
        # get the current bounds
        (xmin, xmax, ymin, ymax, zmin, zmax) = self.getBounds()

        # set the new bounds
        self.setBounds(xmin, top, ymin, right, zmin, back)

        # set the trb variable
        self.trb = (top, right, back)
        return

    def getTRB(self):
        """
        Get the current position of the top, right, back corner
        """
        debugMsg("Called Box.getTRB()")
        return self.trb

    def render(self):
        """
        Perform Box object specific (pre)rendering tasks
        """
        debugMsg("Called Box.render()")
        return


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
        debugMsg("Called ClipBox.setInsideOut()")
        self.insideOut = insideOut
        return

    def getInsideOut(self):
        """
        Get the current value of the inside out flag
        """
        debugMsg("Called ClipBox.getInsideOut()")
        return self.insideOut

    def render(self):
        """
        Perform ClipBox object specific (pre)rendering tasks
        """
        debugMsg("Called ClipBox.render()")
        return



# vim: expandtab shiftwidth=4:
