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
Class and functions associated with a pyvisi Scene
"""

from common import _debug, overrideWarning
from renderer import Renderer

class Scene(object):
    """
    The main object controlling the scene.

    This is the base Scene object.  It should be inherited, and then its 
    methods overridden.  
    """

    def __init__(self):
        """
        The init function
        """
        if _debug: print "\tBASE: Called Scene.__init__()"

        self.renderer = Renderer()
        numCameras = 0

        return

    def add(self, obj):
        """
        Add a new item to the scene

        @param obj: The object to add to the scene
        """
        if _debug: print "\tBASE: Called Scene.add()"

        # print a warning message if get to here
        overrideWarning("Scene.add")

        return

    def place(self, obj):
        """
        Place an object within a scene

        @param obj: The object to place within the scene
        """
        if _debug: print "\tBASE: Called Scene.place()"

        # print a warning message if get to here
        overrideWarning("Scene.place")

        return

    def render(self,pause=False,interactive=False):
        """
        Render (or re-render) the scene
        
        Render the scene, either to screen, or to a buffer waiting for a save

        @param pause: Flag to wait at end of script evaluation for user input
        @param interactive: Whether or not to have interactive use of the output
        """
        if _debug: print "\tBASE: Called Scene.render()"
        renderer = self.renderer

        # I don't yet know where to put this, but just to get stuff going...
        renderer.addToEvalStack("# Scene.render()\n")

        # optionally print out the evaluation stack to make sure we're doing
        # the right thing
        if _debug: print "BASE: Here is the evaluation stack"
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
        if _debug: print "\tBASE: Flusing evaluation stack"
        renderer.resetEvalStack()

        return

    def save(self,file,format):
        """
        Save the scene to a file
        """
        if _debug: print "\tBASE: Called Scene.save()"

        # print a warning message if get to here
        overrideWarning("Scene.save")

        return

    def setBackgroundColor(self,*color):
        """
        Sets the background color of the Scene

        @param color: The color to set the background to.  Can be RGB or CMYK
        """
        if _debug: print "\tBASE: Called Scene.setBackgroundColor()"

        # print a warning message if get to here
        overrideWarning("Scene.setBackgroundColor")

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
        if _debug: print "\tBASE: Called Scene.getBackgroundColor()"

        # print a warning message if get to here
        overrideWarning("Scene.getBackgroundColor")

        return

    def setSize(self, xSize, ySize):
        """
        Sets the size of the scene.

        This size is effectively the renderer window size.

        @param xSize: the size to set the x dimension
        @type xSize: float

        @param ySize: the size to set the y dimension
        @type xSize: float
        """
        if _debug: print "\tBASE: Called Scene.setSize()"

        # print a warning message if get to here
        overrideWarning("Scene.setSize")

        return

    def getSize(self):
        """
        Gets the current size of the scene

        This size is effectively the renderer window size.  Returns a tuple
        of the x and y dimensions respectively, in pixel units(??).
        """
        if _debug: print "\tBASE: Called Scene.getSize()"

        # print a warning message if get to here
        overrideWarning("Scene.getSize")

        return

    def rendererCommand(self,command):
        """
        Allows the user to run a low-level renderer-specific command directly

        @param command: The renderer command to run as a string
        """
        if _debug: print "\tBASE: Called Scene.rendererCommand()"
        evalString = "%s\n" % command
        self.renderer.addToEvalStack(evalString)
        return

# vim: expandtab shiftwidth=4:
