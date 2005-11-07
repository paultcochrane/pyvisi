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
This file contains all of the classes for the various plotting objects.
"""

from pyvisi.renderers.plplot.common import debugMsg

from pyvisi.renderers.plplot.item import Item

__revision__ = '$Revision$'

    
class Plot(Item):
    """
    Abstract plot class
    """

    def __init__(self, scene):
        """
        Initialisation of abstract plot class

        @param scene: The scene with which to associate the plot
        @type scene: Scene object
        """
        debugMsg("Called Plot.__init__()")
        Item.__init__(self)  # initialisation of base class
    
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
    Brief introduction to what the class does
    """

    def __init__(self, arg):
        """
        Brief description of the init function

        @param arg: a description of the argument
        @type arg: the type of the argument
        """
        debugMsg("Called ArrowPlot.__init__()")
        Plot.__init__(self)  # initialisation of base class
    
class ContourPlot(Plot):
    """
    Contour Plots
    """

    def __init__(self, scene):
        """
        Initialisation of the ContourPlot class

        @param arg: The scene with which to associate the plot
        @type arg: Scene object
        """
        debugMsg("Called ContourPlot.__init__()")
        Plot.__init__(self)  # initialisation of base class
        
        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        self.linestyle = None  # pyvisi-defined linestyle
        self._linestyle = None # renderer-specific linestyle
    
        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple
        """
        debugMsg("Called setData() in ContourPlot()")

        self.renderer.runString("# ContourPlot.setData()")

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

        # share around the data
        ## the x data
        self.renderer.renderDict['_x'] = xData

        ## the y data
        self.renderer.renderDict['_y'] = yData

        ## the z data
        self.renderer.renderDict['_z'] = zData

        # determine the min and max of x, y and z
        evalString = "_xMin = min(x)\n"
        evalString += "_xMax = max(x)\n"
        evalString += "_yMin = min(y)\n"
        evalString += "_yMax = max(y)\n"
        evalString += "_zMin = \n"
        evalString += "_zMax = \n"

        ### please complete me!!

        self.renderer.runString(evalString)

        return

    def render(self):
        """
        Does ContourPlot object specific rendering stuff
        """
        debugMsg("Called ContourPlot.render()")

        self.renderer.runString("# ContourPlot.render()")
        self.renderer.runString("_gnuplot('set contour base')")
        self.renderer.runString("_gnuplot('set view 0, 0, 1, 1')")
        self.renderer.runString("_gnuplot('set nosurface')") # gnuplot 3.7

         # if a title is set, put it here
        if self.title is not None:
            evalString = "_gnuplot.title(\'%s\')" % self.title
            self.renderer.runString(evalString)

        # if an xlabel is set, add it
        if self.xlabel is not None:
            evalString = "_gnuplot.xlabel(\'%s\')" % self.xlabel
            self.renderer.runString(evalString)

        # if a ylabel is set, add it
        if self.ylabel is not None:
            evalString = "_gnuplot.ylabel(\'%s\')" % self.ylabel
            self.renderer.runString(evalString)

        self.renderer.runString("_gnuplot('set pm3d')")

        # set up the evalString to use for plotting
        evalString = "_gnuplot.splot(_data)"
        self.renderer.runString(evalString)

        return

class LinePlot(Plot):
    """
    Line Plots
    """

    def __init__(self, scene):
        """
        Initialisation of LinePlot class

        @param arg: The scene with which to associate the plot
        @type arg: Scene object
        """
        debugMsg("Called LinePlot.__init__()")
        Plot.__init__(self, scene)  # initialisation of base class
    
        self.renderer = scene.renderer

        self.title = None
        self.xlabel = None
        self.ylabel = None
        self.zlabel = None

        self.linestyle = None   # pyvisi-defined linestyle
        self._linestyle = None  # renderer-specific linestyle

        # is the LinePlot data offset (vertically) from each other?
        self.offset = False

        # now add the object to the scene
        scene.add(self)

    def setData(self, *dataList, **options):
        """
        Sets the data to the given plot object.

        @param dataList: list of data objects to plot
        @type dataList: tuple

        @param options: keyword options
        @type options: dict
        """
        debugMsg("Called setData() in LinePlot()")
        
        self.renderer.runString("# LinePlot.setData()")

        # grab the options if any
        if options.has_key('offset'):
            self.offset = options['offset']
        else:
            self.offset = False

        # do some sanity checking on the data
        for i in range(len(dataList)):
            if len(dataList[0]) != len(dataList[i]):
                raise ValueError, "Input vectors must all be the same length"

        # this is a really dodgy way to get the data into the renderer
        # I really have to find a better, more elegant way to do this
        
        # if have more than one array to plot, the first one is the x data
        if len(dataList) > 1:
            xData = dataList[0]
            ## pass around the x data
            self.renderer.renderDict['_x'] = xData
            # don't need the first element of the dataList, so get rid of it
            dataList = dataList[1:]
        # if only have one array input, then autogenerate xData
        elif len(dataList) == 1:
            xData = range(1, len(dataList[0])+1)
            if len(xData) != len(dataList[0]):
                errorString = "Autogenerated xData array length not "
                errorString += "equal to input array length"
                raise ValueError, errorString
                        
            ## pass around the x data
            self.renderer.renderDict['_x'] = xData

        # range over the data, printing what the expansion of the array is
        # and regenerate the data within the eval
        for i in range(len(dataList)):
            yDataVar = "_y%d" % i
            data = dataList[i]
            # check that the data here is a 1-D array
            if len(data.shape) != 1:
                raise ValueError, "Can only handle 1D arrays at present"
            
            self.renderer.renderDict[yDataVar] = data

        # if offset is true, then shift the data up accordingly
        if self.offset:
            # concatenate the data
            evalString = "_yAll = concatenate(["
            for i in range(len(dataList)-1):
                evalString += "_y%d," % i
            evalString += "_y%d])" % int(len(dataList)-1)
            self.renderer.runString(evalString)

            # find its min and max
            self.renderer.runString("_yMin = min(_yAll)")
            self.renderer.runString("_yMax = max(_yAll)")

            # keep the data apart a bit with a constant
            self.renderer.runString("_const = 0.1*(_yMax - _yMin)")

            # shift the data up
            self.renderer.runString("_shift = _yMax - _yMin + _const")

            for i in range(len(dataList)):
                evalString = "_y%d = _y%d + %d*_shift" % (i, i, i)
                self.renderer.runString(evalString)

        # determine the min and max of the x and y data
        evalString = "_xMin = min(_x)\n"
        evalString += "_xMax = max(_x)"
        self.renderer.runString(evalString)

        if self.offset:
            ### don't need to recalculate _yMin and _yMax
            # but do need to take into account the shift
            evalString = "_yMax = _yMax + %d*_shift" % len(dataList)
            self.renderer.runString(evalString)
            pass
        else:
            ### but if not offset, do have to

            # concatenate the data
            evalString = "_yAll = concatenate(["
            for i in range(len(dataList)-1):
                evalString += "_y%d," % i
            evalString += "_y%d])" % int(len(dataList)-1)
            self.renderer.runString(evalString)

            # calculate the min and max
            evalString = "_yMin = min(_yAll)\n"
            evalString += "_yMax = max(_yAll)"
            self.renderer.runString(evalString)

        # return the number of data objects to plot
        self.renderer.numDataObjects = len(dataList)

        return

    def render(self):
        """
        Does LinePlot object specific rendering stuff
        """
        debugMsg("Called LinePlot.render()")

        self.renderer.runString("# LinePlot.render()")

        # initialise plplot 
        self.renderer.runString("plplot.plinit()")

        # set up the viewport for plotting
        evalString = "plplot.plenv(_xMin,_xMax,_yMin,_yMax, 0, 1)"
        self.renderer.runString(evalString)

        # set up the evalString to use for plotting
        for i in range(self.renderer.numDataObjects):
            evalString = "plplot.plline(_x, _y%d)" % i
            self.renderer.runString(evalString)

        # if a title is not set, set it to a null string
        # (this will help keep plplot happy)
        if self.title is None:
            self.title = ""

        # if an xlabel is not set, set it to a null string
        if self.xlabel is None:
            self.xlabel = ""

        # if a ylabel is not set, set it to a null string
        if self.ylabel is None:
            self.ylabel = ""

        # put the labels (if any) on the graph.
        evalString = "plplot.pllab(\"%s\", \"%s\", \"%s\")" % \
                (self.xlabel, self.ylabel, self.title)
        self.renderer.runString(evalString)

        # finish stuff off
        self.renderer.runString("plplot.plend()")

        return

    def setLineStyle(self, linestyle):
        """
        Sets the linestyle of the LinePlot

        Linestyles may be either a word in the Gnuplot style, or a symbol 
        shortcut in the Matlab style.  Some of the options do not have a
        Matlab equivalent but do have a Gnuplot equivalent, or vice versa.

        What this method does, is take the linestyles possible as defined by
        PyVisi, and then does some conversion as best it can to get the
        relevant output from (in this case) plplot.
        
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

        self.renderer.runString("# SurfacePlot.setData()")

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

        # pass the data around
        ## the x data
        self.renderer.renderDict['_x'] = xData

        ## the y data
        self.renderer.renderDict['_y'] = yData

        ## the z data
        self.renderer.renderDict['_z'] = zData

        # determine the min and max of x, y and z in world coordinates
        evalString = "_xMin = min(_x)\n"
        evalString += "_xMax = max(_x)\n"
        evalString += "_yMin = min(_y)\n"
        evalString += "_yMax = max(_y)\n"
        evalString += "_zMin = min(_z.flat)\n"
        evalString += "_zMax = max(_z.flat)"
        self.renderer.runString(evalString)

        # min and max of x and y variables in normalised coordinates
        # values are those recommended in plplot documentation for surface
        # plots, and are hardcoded here for the meantime.
        evalString = "_xMin2D = -2.5\n"
        evalString += "_xMax2D = 2.5\n"
        evalString += "_yMin2D = -2.5\n"
        evalString += "_yMax2D = 4.0"
        self.renderer.runString(evalString)

        # sides of the box in normalised coordinates, again, these are those
        # recommended by plplot
        evalString = "_basex = 2.0\n"
        evalString += "_basey = 4.0\n"
        evalString += "_height = 3.0"    # possible name clash???
        self.renderer.runString(evalString)

        # the angle to view the box (this needs to be set up by a Camera()
        # object in the future)
        evalString = "_alt = 45.0\n"
        evalString += "_az = 30.0"
        self.renderer.runString(evalString)

        return

    def render(self):
        """
        Does SurfacePlot object specific rendering stuff
        """
        debugMsg("Called SurfacePlot.render()")

        self.renderer.runString("# SurfacePlot.render()")
        # initialise plplot 
        self.renderer.runString("plplot.plinit()")

        # set up the viewport for plotting
        evalString = "plplot.plenv(_xMin2D,_xMax2D,_yMin2D,_yMax2D, 0, -2)"
        self.renderer.runString(evalString)

        # set up the window
        evalString = "plplot.plw3d(_basex, _basey, _height, "
        evalString += "_xMin, _xMax, _yMin, _yMax, _zMin, _zMax, "
        evalString += "_alt, _az)"
        self.renderer.runString(evalString)

        # if a title is not set, set it to a null string
        # (this will help keep plplot happy)
        if self.title is not None:
            evalString = "plplot.plmtex(\"t\", 1.0, 0.5, 0.5, \"%s\")" % \
                    self.title
            self.renderer.runString(evalString)

        # if an xlabel is not set, set it to a null string
        if self.xlabel is None:
            self.xlabel = ""

        # if a ylabel is not set, set it to a null string
        if self.ylabel is None:
            self.ylabel = ""

        # if a zlabel is not set, set it to a null string
        if self.zlabel is None:
            self.zlabel = ""

        # put the labels (if any) on the graph.
        evalString = "plplot.plbox3(\"bnstu\", \"%s\", 0.0, 0, " % self.xlabel
        evalString += "\"bnstu\", \"%s\", 0.0, 0, " % self.ylabel
        evalString += "\"bcdmnstuv\", \"%s\", 0.0, 0)" % self.zlabel
        self.renderer.runString(evalString)

        # plot it!
        ### note: I can put other shading options into this call
        evalString = "plplot.plsurf3d(_x, _y, _z, 0, ())"
        self.renderer.runString(evalString)

        # finish stuff off
        self.renderer.runString("plplot.plend()")

        # if contours is true, set the relevant option
        if self.contours:
            pass
            # I need to implement this!!!  And put it further up in render()

        return
         
# vim: expandtab shiftwidth=4:
