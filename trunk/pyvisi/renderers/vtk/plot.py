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

# generic imports
from common import _debug, rendererName

# module specific imports
from scene import Scene
from item import Item

class Plot(Scene):
    """
    Abstract plot class
    """
    def __init__(self,scene):
        """
        Initialisation of the abstract Plot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called Plot.__init__()" % rendererName
        pass

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in Plot()" % rendererName
        return True

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self,scene):
        """
        Initialisation of the ArrowPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ArrowPlot.__init__()" % rendererName
        pass

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in ArrowPlot()" % rendererName
        return True

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self,scene):
        """
        Initialisation of the ContourPlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ContourPlot.__init__()" % rendererName
        pass

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in ContourPlot()"%rendererName
        return True

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self,scene):
        """
        Initialisation of the LinePlot class
        
        @param scene: The Scene to render the plot in
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called LinePlot.__init__()" % rendererName

        self.renderer = scene.renderer

        return True

    def setData(self,*dataList):
        """
        Set data to the plot

        @param dataList: List of data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called setData() in LinePlot()" % rendererName

        
        
        return True

# vim: expandtab shiftwidth=4:

