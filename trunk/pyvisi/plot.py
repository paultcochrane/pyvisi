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

## @file plot.py

"""
Class and functions associated with a pyvisi Plot objects
"""

from common import _debug

from item import Item

class Plot(Item):
    """
    Abstract plot class
    """
    def __init__(self):
        if _debug: print "\tBASE: Called Plot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in Plot()"

        # print a warning message if get to here
        overrideWarning("Plot.setData")

        return True

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self):
        if _debug: print "\tBASE: Called ArrowPlot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in ArrowPlot()"

        # print a warning message if get to here
        overrideWarning("ArrowPlot.setData")

        return True

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self):
        if _debug: print "\tBASE: Called ContourPlot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in ContourPlot()"

        # print a warning message if get to here
        overrideWarning("ContourPlot.setData")

        return True

class LinePlot(Plot):
    """
    Line plot

    This is the abstract base class of all LinePlot objects.  Renderer
    modules must inherit and override the methods defined here.
    """
    def __init__(self,scene):
        """
        Initialisation of LinePlot class

        @param scene: the scene with which to associate the LinePlot
        @type scene: Scene object
        """
        if _debug: print "\tBASE: Called LinePlot.__init__()"

        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        self.linestyle = None   # pyvisi-defined linestyle
        self._linestyle = None  # renderer-specific linestyle

        return

    def setData(self,*dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        if _debug: print "\tBASE: Called setData() in LinePlot()"

        # print a warning message if get to here
        overrideWarning("LinePlot.setData")

        return True

# vim: expandtab shiftwidth=4:

