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
Class and functions associated with a pyvisi Plot objects (gnuplot)
"""

# generic imports
from common import _debug, rendererName

# module specific imports
from scene import Scene
from item import Item

class Plot(Scene):
    """
    Abstract plot class
    """
    def __init__(self, scene):
        """
        Initialisation of abstract Plot class

        @param scene: the scene with which to associate the Plot
        """
        if _debug: print "\t%s: Called Plot.__init__()" % rendererName
        return

    def setData(self,data):
        if _debug: print "\t%s: Called setData() in Plot()" % rendererName
        return True

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self,scene):
        """
        Initialisation of ArrowPlot class

        @param scene: the scene with which to associate the ArrowPlot
        """
        if _debug: print "\t%s: Called ArrowPlot.__init__()" % rendererName
        pass

    def setData(self,data):
        if _debug: print "\t%s: Called setData() in ArrowPlot()" % rendererName
        return True

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self,scene):
        """
        Initialisation of ContourPlot class

        @param scene: the scene with which to associate the ContourPlot
        """
        if _debug: print "\t%s: Called ContourPlot.__init__()" % rendererName
        pass

    def setData(self,data):
        if _debug: print "\t%s: Called setData() in ContourPlot()"%rendererName
        return True

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self,scene):
        """
        Initialisation of LinePlot class

        @param scene: the scene with which to associate the LinePlot
        """
        if _debug: print "\t%s: Called LinePlot.__init__()" % rendererName

        self.renderer.addToEvalStack("# LinePlot.__init__()")

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        return

    def setData(self,**data):
        """
        Sets the data to the given plot object.

        @param data: list of data objects to plot
        """
        if _debug: print "\t%s: Called setData() in LinePlot()" % rendererName
        
        self.renderer.addToEvalStack("# LinePlot.setData()")
        dataLen = len(data)
        print "dataLen = %s" % dataLen
        self.renderer.addToEvalStack("_data = Gnuplot.Data(x, y1)")

        return True

# vim: expandtab shiftwidth=4:

