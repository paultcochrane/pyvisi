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
        if _debug: print "\t%s: Called Plot.__init__()" % rendererName
        return

    def setData(self,*dataList):
        """
        Set data to Plot

        @param dataList: the data to set to the plot (should be an array or list
        or something)
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called Plot.setData()" % rendererName
        return True

    def setTitle(self,title):
        """
        Set the plot title

        @param title: the string holding the title to the plot
        @type title: string
        """
        if _debug: print "\t%s: Called Plot.setTitle()" % rendererName

        self.title = title

        return

    def setXLabel(self,label):
        """
        Set the label of the x-axis

        @param label: the string holding the label of the x-axis
        @type label: string
        """
        if _debug: print "\t%s: Called Plot.setXLabel()" % rendererName

        self.xlabel = label

        return

    def setYLabel(self,label):
        """
        Set the label of the y-axis

        @param label: the string holding the label of the y-axis
        @type label: string
        """
        if _debug: print "\t%s: Called Plot.setYLabel()" % rendererName

        self.ylabel = label

        return

    def setZLabel(self,label):
        """
        Set the label of the z-axis

        @param label: the string holding the label of the z-axis
        @type label: string
        """
        if _debug: print "\t%s: Called Plot.setZLabel()" % rendererName

        self.zlabel = label

        return

    def setLabel(self,axis,label):
        """
        Set the label of a given axis

        @param axis: string (Axis object maybe??) of the axis (e.g. x, y, z)

        @param label: string of the label to set for the axis
        @type label: string
        """
        if _debug: print "\t%s: Called Plot.setLabel()" % rendererName

        # string-wise implementation (really budget implementation too)
        if axis == 'x' or axis == 'X':
            self.xlabel = label
        elif axis == 'y' or axis == 'Y':
            self.ylabel = label
        elif axis == 'z' or axis == 'Z':
            self.zlabel = label
        else:
            raise ValueError, "axis must be x or y or z"

        return

class ArrowPlot(Plot):
    """
    Arrow field plot
    """
    def __init__(self,scene):
        """
        Initialisation of ArrowPlot class

        @param scene: the scene with which to associate the ArrowPlot
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ArrowPlot.__init__()" % rendererName
        return

    def setData(self,*dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called ArrowPlot.setData()" % rendererName
        return True

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self,scene):
        """
        Initialisation of ContourPlot class

        @param scene: the scene with which to associate the ContourPlot
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called ContourPlot.__init__()" % rendererName

        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None

        return

    def setData(self,*dataList):
        """
        Sets the data to the Plot

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        if _debug: print "\t%s: Called ContourPlot.setData()"%rendererName
        return True

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self,scene):
        """
        Initialisation of LinePlot class

        @param scene: the scene with which to associate the LinePlot
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called LinePlot.__init__()" % rendererName

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
        if _debug: print "\t%s: Called setData() in LinePlot()" % rendererName
        
        self.renderer.addToEvalStack("# LinePlot.setData()")

        # this is a really dodgy way to get the data into the renderer
        # I really have to find a better, more elegant way to do this

        # for the moment, make sure that there aren't more than two arrays
        if len(dataList) != 2:
            raise ValueError, "Must have two 1D arrays as input (at present)"

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        for i in range(len(dataList)):
            evalString = "_x%d = [" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"
            
            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s]" % data[-1]
            self.renderer.addToEvalStack(evalString)

        evalString = "_data = Gnuplot.Data("
        # loop over all bar the last data element 
        # (the last one doesn't have a trailing comma)
        for i in range(len(dataList)-1):
            evalString += "_x%d, " % i
        evalString += "_x%d" % (len(dataList)-1,)

        # if there are any linestyle settings etc, add them here (gnuplot
        # reasons)
        if self.linestyle is not None:
            # set the linestyle to the renderer-specific version (_linestyle)
            self.setLineStyle(self.linestyle)
            evalString += ", with=\'%s\'" % self._linestyle

        # finish off the evalString
        evalString += ")"

        # and add it to the evalstack
        self.renderer.addToEvalStack(evalString)

        return True

    def render(self):
        """
        Does LinePlot object specific (pre) rendering styff
        """
        if _debug: print "\t%s: Called LinePlot.render()" % rendererName

        self.renderer.addToEvalStack("# LinePlot.render()")

        # if a title is set, put it here
        if self.title is not None:
            evalString = "_gnuplot.title(\'%s\')" % self.title
            self.renderer.addToEvalStack(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_gnuplot.xlabel(\'%s\')" % self.xlabel
            self.renderer.addToEvalStack(evalString)

        # if a ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_gnuplot.ylabel(\'%s\')" % self.ylabel
            self.renderer.addToEvalStack(evalString)

        # if a zlabel is set, add it
        if self.zlabel is not None:
            evalString = "_gnuplot.zlabel(\'%s\')" % self.zlabel
            self.renderer.addToEvalStack(evalString)

        return True

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
        if _debug: print "\t%s: Called LinePlot.setLineStyle()" % rendererName

        # now implement the gnuplot-specific way to do this
        if linestyle == 'lines' or linestyle == '-':
            self._linestyle = 'lines'
        elif linestyle == 'points' or linestyle == 'o':
            self._linestyle = 'points'
        elif linestyle == 'linespoints' or linestyle == '-o':
            self._linestyle = 'linespoints'
        elif linestyle == 'dots' or linestyle == '.':
            self._linestyle = 'dots'
        elif linestyle == 'dotted' or linestyle == ':':
            print "linestyle = %s" % linestyle
            raise NotImplementedError, \
                    "Sorry, haven't implemented this style for %s yet." % \
                    rendererName
        elif linestyle == 'dashes' or linestyle == '--':
            print "linestyle = %s" % linestyle
            raise NotImplementedError, \
                    "Sorry, haven't implemented this style for %s yet." % \
                    rendererName
        elif linestyle == 'dotdashes' or linestyle == '-.':
            print "linestyle = %s" % linestyle
            raise NotImplementedError, \
                    "Sorry, haven't implemented this style for %s yet." % \
                    rendererName
        else:
            raise ValueError, "Unknown linestyle!  I got \'%s\'" % linestyle

        return

    def getLineStyle(self):
        """
        Gets the current linestyle of the LinePlot

        @return: the linestyle as a string
        """
        if _debug: print "\t%s: Called LinePlot.getLineStyle()" % rendererName

        return self.linestyle


# vim: expandtab shiftwidth=4:

