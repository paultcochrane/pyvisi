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

## @file image.py

"""
Class and functions associated with a pyvisi Image objects
"""

# generic imports
from common import _debug, rendererName

# module specific imports
from item import Item

class Image(Item):
    """
    Image class.  Generic class to handle image data.
    """
    def __init__(self,format,scene):
        """
        Initialises the Image class object
        
        @param format: The image format
        @param scene: The Scene object to add to
        """
        if _debug: print "\t%s: Called Image.__init__()" % rendererName

        if format == "jpeg":
            if _debug: print "\t%s: Using jpeg image format" % rendererName
            return JpegImage(scene)
        else:
            print "Unknown image format %s" % format
            return None
        
        return

    def load(self, file):
        """
        Loads image data from file.

        @param file: The filename from which to load image data
        """
        if _debug: print "\t%s: Called Image.load()" % rendererName
        return

class JpegImage(Image):
    """
    Subclass of Image class to explicitly handle jpeg images
    """
    def __init__(self, scene):
        """
        Initialises the JpegImage class object

        @param scene: The Scene object to add to
        """
        if _debug: print "\t%s: Called JpegImage.__init__()" % rendererName
        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# JpegImage.__init__()")
        self.renderer.addToEvalStack("_jpegReader = vtk.vtkJPEGReader()")
        self.readerName = "_jpegReader"
        
        return

    def load(self, file):
        """
        Loads jpeg image data from file.

        @param file: The filename from which to load jpeg image data
        """
        if _debug: print "\t%s: Called JpegImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# JpegImage.load()")
        evalString = "_jpegReader.SetFileName(\"%s\")" % file
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does JpegImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called JpegImage.render()" % rendererName

        self.renderer.addToEvalStack("# JpegImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_jpegReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return

class PngImage(Image):
    """
    Subclass of Image class to explicitly handle png images
    """
    def __init__(self, scene):
        """
        Initialises the PngImage class object

        @param scene: The Scene object to add to
        @type scene: scene object
        """
        if _debug: print "\t%s: Called PngImage.__init__()" % rendererName
        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# PngImage.__init__()")
        self.renderer.addToEvalStack("_pngReader = vtk.vtkPNGReader()")
        self.readerName = "_pngReader"
        
        return

    def load(self, file):
        """
        Loads png image data from file.

        @param file: The filename from which to load png image data
        """
        if _debug: print "\t%s: Called PngImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# PngImage.load()")
        evalString = "_pngReader.SetFileName(\"%s\")" % file
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does PngImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called PngImage.render()" % rendererName

        self.renderer.addToEvalStack("# PngImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_pngReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return

# vim: expandtab shiftwidth=4:
