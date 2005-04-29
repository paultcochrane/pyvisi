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

## @file scene.py

"""
Class and functions associated with a pyvisi Scene
"""

# generic imports
from pyvisi.renderers.vtk.common import debugMsg
from pyvisi.scene import Scene as BaseScene

# module specific imports
from pyvisi.renderers.vtk.renderer import Renderer

__revision__ = '$Revision$'

class Scene(BaseScene):
    """
    The main object controlling the scene.
    
    Scene object methods and classes overriding the BaseScene class.
    """

    def __init__(self):
        """
        The init function
        """
        debugMsg("Called Scene.__init__()")
        BaseScene.__init__(self)

        self.renderer = Renderer()

        self.xSize = 640
        self.ySize = 480

        self.objectList = []

    def add(self, obj):
        """
        Add a new item to the scene

        @param obj: The object to add to the scene
        @type obj: object
        """
        debugMsg("Called Scene.add()")

        if obj is None:
            raise ValueError, "You must specify an object to add"

        self.objectList.append(obj)

        return

    def place(self, obj):
        """
        Place an object within a scene

        @param obj: The object to place within the scene
        @type obj: object
        """
        debugMsg("Called Scene.place()")

        if obj is None:
            raise ValueError, "You must specify an object to place"

        return

    def render(self, pause=False, interactive=False, save=False):
        """
        Render (or re-render) the scene
        
        Render the scene, either to screen, or to a buffer waiting for a save

        @param pause: Flag to wait at end of script evaluation for user input
        @type pause: boolean

        @param interactive: Whether or not to have interactive use of the output
        @type interactive: boolean
        """
        debugMsg("Called Scene.render()")
        renderer = self.renderer

        # I don't yet know where to put this, but just to get stuff going...
        renderer.addToEvalStack("# Scene.render()")

        if interactive:
            renderer.addToEvalStack(\
                    "_iRenderer = vtk.vtkRenderWindowInteractor()")
            renderer.addToEvalStack(\
                    "_iRenderer.SetRenderWindow(_renderWindow)")

        # get all objects in the scene to render themselves
        for obj in self.objectList:
            obj.render()

        # if saving to file, try not to render to the screen
        if save:
            renderer.addToEvalStack("_renderWindow.OffScreenRenderingOn()")
            renderer.addToEvalStack("_renderWindow.Render()")
        else:
            renderer.addToEvalStack("_renderWindow.Render()")

        if interactive:
            renderer.addToEvalStack("_iRenderer.Start()")

        # write it
        if save:
            self.renderer.addToEvalStack("_outWriter.Write()")

        # add some code to pause after rendering if asked to
        if pause:
            renderer.addToEvalStack("raw_input(\"Press enter to continue\")")

        # prepend the init stack to the eval stack
        self.renderer._evalStack = self.renderer._initStack + \
                self.renderer._evalStack

        # optionally print out the evaluation stack to make sure we're doing
        # the right thing
        debugMsg("Here is the evaluation stack")
        debugMsg(60*"#")
        debugMsg(renderer.getEvalStack())
        debugMsg(60*"#")

        # now compile the string object into code, and execute it
        try:
            compileObj = compile(renderer.getEvalStack(), \
                    'compileErrs.txt', 'exec')
            exec compileObj
        except LookupError:
            print "evalStack execution failed"
            print "evalStack = \'%s\'" % renderer.getEvalStack()
            return None

        # flush the evaluation stack
        debugMsg("Flushing evaluation stack")
        renderer.resetEvalStack()

        return

    def save(self, fname, format):
        """
        Save the scene to a file

        Possible formats are:
            - Postscript
            - PNG
            - JPEG
            - TIFF
            - BMP
            - PNM

        @param fname: Name of output file
        @type fname: string

        @param format: Graphics format of output file
        @type format: Image object or string
        """
        debugMsg("Called Scene.save()")
        self.renderer.addToEvalStack("# Scene.save()")

        # if the format is passed in as a string or object, react
        # appropriately
        import types
        if type(format) is types.StringType:
            fmt = format.lower()
        else:
            fmt = format.format

        # need to pass the render window through a filter to an image object
        self.renderer.addToEvalStack(
                "_win2imgFilter = vtk.vtkWindowToImageFilter()")
        self.renderer.addToEvalStack("_win2imgFilter.SetInput(_renderWindow)")

        # set the output format
        if fmt == "ps":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkPostScriptWriter()")
        elif fmt == "png":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkPNGWriter()")
        elif fmt == "jpeg" or fmt == "jpg":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkJPEGWriter()")
        elif fmt == "tiff" or fmt == "tif":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkTIFFWriter()")
        elif fmt == "bmp":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkBMPWriter()")
        elif fmt == "pnm":
            self.renderer.addToEvalStack(
                    "_outWriter = vtk.vtkPNMWriter()")
        else:
            raise ValueError, "Unknown graphics format.  I got %s" % fmt

        # set stuff up to write
        self.renderer.addToEvalStack(
                "_outWriter.SetInput(_win2imgFilter.GetOutput())")
        evalString = "_outWriter.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        
        # rerender the scene to get the output
        self.render(save=True)

        return

    # set up an alias for the save method
    write = save

    def setBackgroundColor(self, *color):
        """
        Sets the background color of the Scene

        @param color: The color to set the background to.  Can be RGB or CMYK
        @type color: tuple
        """
        debugMsg("Called Scene.setBackgroundColor()")

        # pity this code doesn't work....
        # need to check on the values given in the *color array.
        # if they're greater than 1, scale so that the largest is 1
        #maxColor = None
        #for i in range(len(color)):
            #if color[i] > 1:
                #maxColor = color[i]
                #print maxColor
#
        ## if a maximum colour is found, then scale the colours
        #if maxColor is not None:
            #for i in range(len(color)):
                #color[i] = color[i]/maxColor
        
        # if color is of length 3, then we have rgb
        # if length is 4 then cmyk
        # if length is 1 then greyscale
        # otherwise barf
        if len(color) == 3:
            # ok, using rgb
            # probably should use a Color object or something
            # this will do in the meantime
            evalString = "_renderer.SetBackground(%f,%f,%f)" % \
                    (color[0], color[1], color[2])
            self.renderer.addToEvalStack(evalString)
        else:
            raise ValueError, "Sorry, only RGB color is supported at present"

        return

    def getBackgroundColor(self):
        """
        Gets the current background color setting of the Scene
        """
        debugMsg("Called Scene.getBackgroundColor()")
        return

    def setSize(self, xSize, ySize):
        """
        Sets the size of the scene.

        This size is effectively the renderer window size.

        @param xSize: the size to set the x dimension
        @type xSize: float

        @param ySize: the size to set the y dimension
        @type ySize: float
        """
        debugMsg("Called Scene.setSize()")

        self.xSize = xSize
        self.ySize = ySize
        
        return

    def getSize(self):
        """
        Gets the current size of the scene

        This size is effectively the renderer window size.  Returns a tuple
        of the x and y dimensions respectively, in pixel units(??).
        """
        debugMsg("Called Scene.getSize()")
        return (self.xSize, self.ySize)


# vim: expandtab shiftwidth=4:
