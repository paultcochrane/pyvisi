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

        self.renderer = scene.renderer

    def render(self):
        """
        Perform Box object specific (pre)rendering tasks
        """
        debugMsg("Called Box.render()")


class CutBox(Box):
    """
    Class for boxes used to cut through datasets
    """

    def __init__(self, scene):
        """
        Intialisation of the CutBox object
        """
        debugMsg("Called CutBox.__init__()")
        Plane.__init__(self)

        self.renderer = scene.renderer


class ClipBox(Box):
    """
    Class for boxes used to clip datasets
    """

    def __init__(self, scene):
        """
        Intialisation of the ClipBox object
        """
        debugMsg("Called ClipBox.__init__()")
        Plane.__init__(self)

        self.renderer = scene.renderer


# vim: expandtab shiftwidth=4:
