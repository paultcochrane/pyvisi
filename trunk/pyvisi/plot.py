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
Base class and functions associated with a pyvisi Plot objects
"""

from common import _debug

from item import Item

class Plot(Item):
    """
    Abstract plot class
    """
    def __init__(self, scene):
        """
        Initialisation of abstract Plot class

        @param scene: the scene with which to associate the Plot
        @type scene: Scene object
        """
        if _debug: print "\tBASE: Called Plot.__init__()"

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        return

    def setData(self,data):
        """
        Set data to Plot

        @param dataList: the data to set to the plot
        @type dataList: tuple
        """
        if _debug: print "\tBASE: Called setData() in Plot()"

        # print a warning message if get to here
        overrideWarning("Plot.setData")

        return True

    def setTitle(self,title):
        """
        Set the plot title

        @param title: the string holding the title to the plot
        @type title: string
        """
        if _debug print "\tBASE: Called Plot.setTitle()"

        self.title = title

        return

    def setXLabel(self,label):
        """
        Set the label of the x-axis

        @param label: the string holding the label of the x-axis
        @type label: string
        """
        if _debug: print "\tBASE: Called Plot.setXLabel()"

        self.xlabel = label

        return

    def setYLabel(self,label):
        """
        Set the label of the y-axis

        @param label: the string holding the label of the y-axis
        @type label: string
        """
        if _debug: print "\tBASE: Called Plot.setYLabel()"

        self.ylabel = label

        return

    def setZLabel(self,label):
        """
        Set the label of the z-axis

        @param label: the string holding the label of the z-axis
        @type label: string
        """
        if _debug: print "\tBASE: Called Plot.setZLabel()"

        self.zlabel = label

        return

    def setLabel(self,axis,label):
        """
        Set the label of a given axis

        @param axis: string (Axis object maybe??) of the axis (e.g. x, y, z,)

        @param label: string of the label to set for the axis
        @type label: string
        """
        if _debug: print "\tBASE: Called Plot.setLabel()"

        # string-wise implementation
        if axis == 'x' or axis == 'X':
            self.xlabel = label
        elif axis = 'y' or axis == 'Y':
            self.ylabel = label
        elif axis = 'z' or axis == 'Z':
            self.zlabel = label
        else:
            raise ValueError, "axis must be x or y or z"

        return

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

    def render(self):
        """
        Does LinePlot object specific (pre) rendering stuff
        """
        if _debug: print "\tBASE: Called LinePlot.render()"

        # print a warning message if get to here
        overrideWarning("LinePlot.render")

        return

    def setLineStyle(self,linestyle):
        """
         Sets the linestyle of the LinePlot

         Linestyles may be either a word in the Gnuplot style, or a symbol 
         shortcut in the Matlab style.  Some of the options do not have a
         Matlab equivalent but do have a Gnuplot equivalent, or vice versa.

         What this method does, is take the linestyles possible as defined by
         PyVisi, and then does some conversion as best it can to get the
         relevant output from (in this case) gnuplot.  

         Possible linestyles are:
             1. lines ('-')
             2. points ('o')
             3. linespoints ('-o')
             4. dots ('.')
             5. dotted (':')
             6. dashes ('--')
             7. dotdashes ('-.')

         @param linestyle: the style to use for the lines
         @type linestyle: string
         """
         if _debug: print "\tBASE: Called LinePlot.setLineStyle()"

         # print a warning if get to here
         overrideWarning("LinePlot.setLineStyle")

         return

     def getLineStyle(self):
         """
         Gets the current linestyle of the LinePlot

         @return: the linestyle as a string
         """
         if _debug: print "\tBASE: Called LinePlot.getLineStyle()"

         return self.linestyle

# vim: expandtab shiftwidth=4:

