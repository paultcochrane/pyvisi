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

## @file plot.py

"""
Class and functions associated with a pyvisi Plot objects (gnuplot)
"""

# generic imports
from pyvisi.renderers.gnuplot.common import debugMsg, _gnuplot4

# module specific imports
from pyvisi.renderers.gnuplot.item import Item

__revision__ = '$Revision$'

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
        debugMsg("Called Plot.__init__()")
        Item.__init__(self)

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Set data to Plot

        @param dataList: the data to set to the plot (should be an array or list
        or something)
        @type dataList: tuple
        """
        debugMsg("Called Plot.setData()")

        if dataList is None:
            raise ValueError, "You must specify a data list"
        
        return

    def setTitle(self, title):
        """
        Set the plot title

        @param title: the string holding the title to the plot
        @type title: string
        """
        debugMsg("Called Plot.setTitle()")

        self.title = title

        return

    def setXLabel(self, label):
        """
        Set the label of the x-axis

        @param label: the string holding the label of the x-axis
        @type label: string
        """
        debugMsg("Called Plot.setXLabel()")

        self.xlabel = label

        return

    def setYLabel(self, label):
        """
        Set the label of the y-axis

        @param label: the string holding the label of the y-axis
        @type label: string
        """
        debugMsg("Called Plot.setYLabel()")

        self.ylabel = label

        return

    def setZLabel(self, label):
        """
        Set the label of the z-axis

        @param label: the string holding the label of the z-axis
        @type label: string
        """
        debugMsg("Called Plot.setZLabel()")

        self.zlabel = label

        return

    def setLabel(self, axis, label):
        """
        Set the label of a given axis

        @param axis: string (Axis object maybe??) of the axis (e.g. x, y, z)

        @param label: string of the label to set for the axis
        @type label: string
        """
        debugMsg("Called Plot.setLabel()")

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
    def __init__(self, scene):
        """
        Initialisation of ArrowPlot class

        @param scene: the scene with which to associate the ArrowPlot
        @type scene: Scene object
        """
        debugMsg("Called ArrowPlot.__init__()")
        Plot.__init__(self, scene)

        if scene is None:
            raise ValueError, "You must specify a scene object"

    def setData(self, *dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called ArrowPlot.setData()")

        if dataList is None:
            raise ValueError, "You must specify a data List"
        
        return

class ContourPlot(Plot):
    """
    Contour plot
    """
    def __init__(self, scene):
        """
        Initialisation of ContourPlot class

        @param scene: the scene with which to associate the ContourPlot
        @type scene: Scene object
        """
        debugMsg("Called ContourPlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None

        # now add the plot to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Sets the data to the Plot

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called ContourPlot.setData()")

        self.renderer.addToEvalStack("# ContourPlot.setData()")

        # this is a really dodgy way to get the data into the renderer
        # I really have to find a better, more elegant way to do this

        # for the moment, make sure that there are three arrays
        if len(dataList) != 3:
            raise ValueError, "Must have three arrays as input (at present)"

        # do some sanity checks on the data
        xData = dataList[0]
        yData = dataList[1]
        zData = dataList[2]

        if len(xData.shape) != 1:
            raise ValueError, "x data array is not of correct shape: %s" % \
                    xData.shape

        if len(yData.shape) != 1:
            raise ValueError, "y data array is not of correct shape: %s" % \
                    yData.shape

        if len(zData.shape) != 2:
            raise ValueError, "z data array is not of correct shape: %s" % \
                    zData.shape

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        ## the x data
        evalString = "_x = ["
        for j in range(len(xData)-1):
            evalString += "%s, " % xData[j]
        evalString += "%s]" % xData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the y data
        evalString = "_y = ["
        for j in range(len(yData)-1):
            evalString += "%s, " % yData[j]
        evalString += "%s]" % yData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the z data
        evalString = "_z = ["
        for i in range(len(xData)):
            evalString += "["
            for j in range(len(yData)-1):
                evalString += "%s, " % zData[i, j]
            evalString += "%s],\n" % zData[i, -1]
        evalString += "]"
        self.renderer.addToEvalStack(evalString)

        self.renderer.addToEvalStack(\
                "_data = Gnuplot.GridData(_z, _x, _y, binary=0)")

        return

    def render(self):
        """
        Does ContourPlot object specific rendering stuff
        """
        debugMsg("Called ContourPlot.render()")

        self.renderer.addToEvalStack("# ContourPlot.render()")
        self.renderer.addToEvalStack("_gnuplot('set contour base')")
        self.renderer.addToEvalStack("_gnuplot('set view 0, 0, 1, 1')")
        self.renderer.addToEvalStack("_gnuplot('set nosurface')") # gnuplot 3.7

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

        # gnuplot 4 specific (I reckon I should bite the bullet with this
        # one)
        if _gnuplot4:
            self.renderer.addToEvalStack("_gnuplot('set pm3d')")

        # set up the evalString to use for plotting
        evalString = "_gnuplot.splot(_data)"
        self.renderer.addToEvalStack(evalString)

        return

class LinePlot(Plot):
    """
    Line plot
    """
    def __init__(self, scene):
        """
        Initialisation of LinePlot class

        @param scene: the scene with which to associate the LinePlot
        @type scene: Scene object
        """
        debugMsg("Called LinePlot.__init__()")
        Plot.__init__(self, scene)

        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        self.linestyle = None   # pyvisi-defined linestyle
        self._linestyle = None  # renderer-specific linestyle

        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in LinePlot()")
        
        self.renderer.addToEvalStack("# LinePlot.setData()")

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # this is a really dodgy way to get the data into the renderer
        # I really have to find a better, more elegant way to do this
        
        # if have more than one array to plot, the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## generate the evalString for the x data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
        # if only have one array input, then autogenerate xData
        elif len(dataList) == 1:
            xData = range(1, len(dataList[0])+1)
            if len(xData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString
                        
            ## generate the evalString for the x data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
            # send it to the renderer
            self.renderer.addToEvalStack(evalString)

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        for i in range(len(dataList)):
            evalString = "_y%d = [" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"
            
            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s]" % data[-1]
            self.renderer.addToEvalStack(evalString)

            evalString = "_data%d = Gnuplot.Data(_x, " % i
            evalString += "_y%d" % i

            # if there are any linestyle settings etc, add them here (gnuplot
            # reasons)
            if self.linestyle is not None:
                # set the linestyle to renderer-specific version (_linestyle)
                self.setLineStyle(self.linestyle)
                evalString += ", with=\'%s\'" % self._linestyle

            # finish off the evalString
            evalString += ")"

            # and add it to the evalstack
            self.renderer.addToEvalStack(evalString)

        # return the number of data objects to plot
        self.renderer.numDataObjects = len(dataList)

        return

    def render(self):
        """
        Does LinePlot object specific rendering stuff
        """
        debugMsg("Called LinePlot.render()")

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

        # set up the evalString to use for plotting
        evalString = "_gnuplot.plot("
        for i in range(self.renderer.numDataObjects-1):
            evalString += "_data%d, " % i
        evalString += "_data%d)" % (self.renderer.numDataObjects-1,)
        self.renderer.addToEvalStack(evalString)

        return

    def setLineStyle(self, linestyle):
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
        debugMsg("Called LinePlot.setLineStyle()")

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
                    "Sorry, haven't implemented this style yet."
        elif linestyle == 'dashes' or linestyle == '--':
            print "linestyle = %s" % linestyle
            raise NotImplementedError, \
                    "Sorry, haven't implemented this style yet."
        elif linestyle == 'dotdashes' or linestyle == '-.':
            print "linestyle = %s" % linestyle
            raise NotImplementedError, \
                    "Sorry, haven't implemented this style yet."
        else:
            raise ValueError, "Unknown linestyle!  I got \'%s\'" % linestyle

        return

    def getLineStyle(self):
        """
        Gets the current linestyle of the LinePlot

        @return: the linestyle as a string
        """
        debugMsg("Called LinePlot.getLineStyle()")

        return self.linestyle

class ScatterPlot(Plot):
    """
    Scatter plot 
    
    Plots a scatter data points in 2D, for 3D scatter plots use ScatterPlot3D
    """

    def __init__(self, scene):
        """
        Initialisation of ScatterPlot class

        @param scene: the scene with which to associate the ScatterPlot
        @type scene: Scene object
        """
        debugMsg("Called ScatterPlot.__init__()")
        Plot.__init__(self, scene)

        # grab the renderer
        self.renderer = scene.renderer

        # set up some of the attributes
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None
        
        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ScatterPlot()")

        self.renderer.addToEvalStack("# ScatterPlot.setData()")

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # if have more than one array to plot the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## generate the evalString for the data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
            # give it to the renderer
            self.renderer.addToEvalStack(evalString)
            # don't need the first element of the dataList so get rid of it
            dataList = dataList[1:]
        # if only have one array input, then autogenerate the xData
        elif len(dataList) == 1:
            xData = range(1, len(dataList[0])+1)
            if len(xData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString

            ## generate the evalString for the x data
            evalString = "_x = ["
            for j in range(len(xData)-1):
                evalString += "%s, " % xData[j]
            evalString += "%s]" % xData[-1]
            # send it to the renderer
            self.renderer.addToEvalStack(evalString)

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        for i in range(len(dataList)):
            evalString = "_y%d = [" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"

            for j in range(len(data)-1):
                evalString += "%s, " % data[j]
            evalString += "%s]" % data[-1]
            self.renderer.addToEvalStack(evalString)

            evalString = "_data%d = Gnuplot.Data(_x, " % i
            evalString += "_y%d" % i

            # this is the linestyle that makes this a scatter plot
            evalString += ", with='points pointtype 2'"

            # finish off the evalString
            evalString += ")"

            # and add it to the evalstack
            self.renderer.addToEvalStack(evalString)

        # return the number of objects to plot
        self.renderer.numDataObjects = len(dataList)

        return

    def render(self):
        """
        Does ScatterPlot object specific rendering stuff
        """
        debugMsg("Called ScatterPlot.render()")

        self.renderer.addToEvalStack("# ScatterPlot.render()")

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
            evalString = "_gnuplot('set zlabel \\'%s\\'')" % self.zlabel
            self.renderer.addToEvalStack(evalString)

        # set up the evalString to use for plotting
        evalString = "_gnuplot.plot("
        for i in range(self.renderer.numDataObjects-1):
            evalString += "_data%d, " % i
        evalString += "_data%d)" % (self.renderer.numDataObjects-1,)
        self.renderer.addToEvalStack(evalString)

        return

class ScatterPlot3D(Plot):
    """
    Scatter Plot in three dimensions.

    This is like a surface plot, but using crosses, or points as the data
    points.
    """

    def __init__(self, scene):
        """
        Initialisation of ScatterPlot3D class

        @param scene: the scene with which to associate the ScatterPlot3D
        @type scene: Scene object
        """
        debugMsg("Called ScatterPlot3D.__init__()")
        Plot.__init__(self, scene)

        # grab the renderer
        self.renderer = scene.renderer

        # set up some of the attributes
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ScatterPlot3D()")

        self.renderer.addToEvalStack("# ScatterPlot3D.setData()")

        # for the moment, make sure that there are three arrays
        if len(dataList) != 3:
            raise ValueError, "Must have three arrays as input (at present)"

        # do some sanity checks on the data
        xData = dataList[0]
        yData = dataList[1]
        zData = dataList[2]

        if len(xData.shape) != 1:
            raise ValueError, "x data array is not of the correct shape: %s"\
                    % xData.shape

        if len(yData.shape) != 1:
            raise ValueError, "y data array is not of the correct shape: %s"\
                    % yData.shape

        if len(zData.shape) != 2:
            raise ValueError, "z data array is not of the correct shape: %s"\
                    % zData.shape

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        ## the x data
        evalString = "_x = ["
        for j in range(len(xData)-1):
            evalString += "%s, " % xData[j]
        evalString += "%s]" % xData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the y data
        evalString = "_y = ["
        for j in range(len(yData)-1):
            evalString += "%s, " % yData[j]
        evalString += "%s]" % yData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the z data
        evalString = "_z = ["
        for i in range(len(xData)):
            evalString += "["
            for j in range(len(yData)-1):
                evalString += "%s, " % zData[i, j]
            evalString += "%s],\n" % zData[i, -1]
        evalString += "]"
        self.renderer.addToEvalStack(evalString)

        self.renderer.addToEvalStack(\
                "_data = Gnuplot.GridData(_z, _x, _y, binary=0)")

        return

    def render(self):
        """
        Does ScatterPlot3D object specific rendering stuff
        """
        debugMsg("Called ScatterPlot3D.render()")

        self.renderer.addToEvalStack("# ScatterPlot3D.render()")
        if _gnuplot4:
            evalString = "_gnuplot('set style data points')"
            self.renderer.addToEvalStack(evalString)
        else:
            evalString = "_gnuplot('set data style points')"
            self.renderer.addToEvalStack(evalString)

        #self.renderer.addToEvalStack("_gnuplot('set surface')")

        # if a title is set, put it here
        if self.title is not None:
            evalString = "_gnuplot.title(\'%s\')" % self.title
            self.renderer.addToEvalStack(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_gnuplot.xlabel(\'%s\')" % self.xlabel
            self.renderer.addToEvalStack(evalString)

        # if a ylabel is set add it
        if self.ylabel is not None:
            evalString = "_gnuplot.ylabel(\'%s\')" % self.ylabel
            self.renderer.addToEvalStack(evalString)

        # if a zlabel is set add it
        if self.zlabel is not None:
            evalString = "_gnuplot('set zlabel \\'%s\\'')" % self.zlabel
            self.renderer.addToEvalStack(evalString)

        # set up the evalString to use for plotting
        evalString = "_gnuplot.splot(_data)"
        self.renderer.addToEvalStack(evalString)

        return

class SurfacePlot(Plot):
    """
    Surface plot
    """

    def __init__(self, scene):
        """
        Initialisation of SurfacePlot class

        @param scene: the scene with which to associate the SurfacePlot
        @type scene: Scene object
        """
        debugMsg("Called SurfacePlot.__init__()")
        Plot.__init__(self, scene)

        # grab the renderer
        self.renderer = scene.renderer

        # set up some of the attributes
        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        # to show contours of the surface on the bottom of the axes, set
        # this variable to True
        self.contours = False

        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in SurfacePlot()")

        self.renderer.addToEvalStack("# SurfacePlot.setData()")

        # for the moment, make sure that there are three arrays
        if len(dataList) != 3:
            raise ValueError, "Must have three arrays as input (at present)"

        # do some sanity checks on the data
        xData = dataList[0]
        yData = dataList[1]
        zData = dataList[2]

        if len(xData.shape) != 1:
            raise ValueError, "x data array is not of the correct shape: %s"\
                    % xData.shape

        if len(yData.shape) != 1:
            raise ValueError, "y data array is not of the correct shape: %s"\
                    % yData.shape

        if len(zData.shape) != 2:
            raise ValueError, "z data array is not of the correct shape: %s"\
                    % zData.shape

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        ## the x data
        evalString = "_x = ["
        for j in range(len(xData)-1):
            evalString += "%s, " % xData[j]
        evalString += "%s]" % xData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the y data
        evalString = "_y = ["
        for j in range(len(yData)-1):
            evalString += "%s, " % yData[j]
        evalString += "%s]" % yData[-1]
        self.renderer.addToEvalStack(evalString)

        ## the z data
        evalString = "_z = ["
        for i in range(len(xData)):
            evalString += "["
            for j in range(len(yData)-1):
                evalString += "%s, " % zData[i, j]
            evalString += "%s],\n" % zData[i, -1]
        evalString += "]"
        self.renderer.addToEvalStack(evalString)

        self.renderer.addToEvalStack(\
                "_data = Gnuplot.GridData(_z, _x, _y, binary=0)")

        return

    def render(self):
        """
        Does SurfacePlot object specific rendering stuff
        """
        debugMsg("Called SurfacePlot.render()")

        self.renderer.addToEvalStack("# SurfacePlot.render()")
        self.renderer.addToEvalStack("_gnuplot('set surface')")

        # if a title is set, put it here
        if self.title is not None:
            evalString = "_gnuplot.title(\'%s\')" % self.title
            self.renderer.addToEvalStack(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_gnuplot.xlabel(\'%s\')" % self.xlabel
            self.renderer.addToEvalStack(evalString)

        # if a ylabel is set add it
        if self.ylabel is not None:
            evalString = "_gnuplot.ylabel(\'%s\')" % self.ylabel
            self.renderer.addToEvalStack(evalString)

        # if a zlabel is set add it
        if self.zlabel is not None:
            evalString = "_gnuplot('set zlabel \\'%s\\'')" % self.zlabel
            self.renderer.addToEvalStack(evalString)

        if not _gnuplot4:
            evalString = "_gnuplot('set data style lines')"
            self.renderer.addToEvalStack(evalString)

        # if contours is true, set the relevant option
        if self.contours:
            evalString = "_gnuplot('set contour base')"
            self.renderer.addToEvalStack(evalString)

        # this is gnuplot 4 specific, maybe should deprecate gnuplot 3.7...
        if _gnuplot4:
            self.renderer.addToEvalStack("_gnuplot('set pm3d')")

        # set up the evalString to use for plotting
        evalString = "_gnuplot.splot(_data)"
        self.renderer.addToEvalStack(evalString)

        return
            
# vim: expandtab shiftwidth=4:

