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

## @file scene.py

"""
Class and functions associated with a pyvisi Scene (gnuplot)
"""

# generic imports
from common import _debug, rendererName, rendererVersion
from pyvisi.scene import Scene as BaseScene

# module specific imports
from renderer import Renderer

class Scene(BaseScene):
    """
    The main object controlling the scene.
    
    Scene object methods and classes overriding the BaseScene class.
    """

    def __init__(self):
        """
        The init function
        """
        print "You are using PyVisi renderer module \"%s\" version %s" % \
                (rendererName, rendererVersion)

        if _debug: print "\t%s: Called Scene.__init__()" % rendererName

        self.renderer = Renderer()

        # kept around in the hope that it will be useful...
        numCameras = 0

        return

    def add(self, obj):
        """
        Add a new item to the scene

        @param obj: The object to add to the scene
        @type obj: object
        """
        if _debug: print "\t%s: Called Scene.add()" % rendererName
        self.renderer.addToEvalStack("# Scene.add()")

        return

    def place(self, obj):
        """
        Place an object within a scene

        @param obj: The object to place within the scene
        @type obj: object
        """
        if _debug: print "\t%s: Called Scene.place()" % rendererName
        return

    def render(self,pause=False,interactive=False):
        """
        Render (or re-render) the scene
        
        Render the scene, either to screen, or to a buffer waiting for a save

        @param pause: Flag to wait at end of script evaluation for user input
        @type pause: boolean

        @param interactive: Whether or not to have interactive use of the 
        output (not available in all renderer modules)
        @type interactive: boolean
        """
        if _debug: print "\t%s: Called Scene.render()" % rendererName
        renderer = self.renderer

        renderer.addToEvalStack("# Scene.render()")
        # set up the evalString to use for plotting
        evalString = "_gnuplot.plot("
        for i in range(self.renderer.numDataObjects-1):
            evalString += "_data%d, " % i
        evalString += "_data%d)" % (self.renderer.numDataObjects-1,)
        renderer.addToEvalStack(evalString)

        # add some code to pause after rendering if asked to
        if pause:
            renderer.addToEvalStack("raw_input(\"Press enter to continue\")")

        # optionally print out the evaluation stack to make sure we're doing
        # the right thing
        if _debug: print "\t%s: Here is the evaluation stack" % rendererName
        if _debug: print 70*"#"
        if _debug: print renderer.getEvalStack()
        if _debug: print 70*"#"

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
        #if _debug: print "\t%s: Flusing evaluation stack" % rendererName
        #renderer.resetEvalStack()

        return

    def save(self,file,format):
        """
        Save the scene to a file

        Possible formats are:
            - Postscript
            - PNG
            - PBM

        @param file: Name of output file
        @type file: string

        @param format: Graphics format of output file
        @type format: string
        """
        if _debug: print "\t%s: Called Scene.save()" % rendererName
        self.renderer.addToEvalStack("# Scene.save()")

        # set the output format
        if format == "PS":
            self.renderer.addToEvalStack("_gnuplot('set terminal postscript')")
        elif format == "PNG":
            self.renderer.addToEvalStack("_gnuplot('set terminal png')")
        elif format == "PBM":
            self.renderer.addToEvalStack("_gnuplot('set terminal pbm')")
        else:
            raise ValueError, "Unknown graphics format."

        # set the output filename
        evalString = "_gnuplot('set output \"%s\"')" % file
        self.renderer.addToEvalStack(evalString)

        # now render the whole shebang (again)
        self.render()

        return

    def setBackgroundColor(self,*color):
        """
        Sets the background color of the Scene

        @param color: The color to set the background to.  Can be RGB or CMYK
        @type color: tuple
        """
        if _debug: print "\t%s: Called Scene.setBackgroundColor()"%rendererName

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
            pass
        else:
            raise UserError, "Sorry, only RGB color is supported at present"

        return

    def getBackgroundColor(self):
        """
        Gets the current background color setting of the Scene
        """
        if _debug: print "\t%s: Called Scene.getBackgroundColor()"%rendererName
        return

# vim: expandtab shiftwidth=4:
