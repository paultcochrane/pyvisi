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

class BmpImage(Image):
    """
    Subclass of Image class to explicitly handle bmp images
    """
    def __init__(self, scene):
        """
        Initialises the BmpImage class object

        @param scene: The Scene object to add to
        @type scene: scene object
        """
        if _debug: print "\t%s: Called BmpImage.__init__()" % rendererName
        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# BmpImage.__init__()")
        self.renderer.addToEvalStack("_bmpReader = vtk.vtkBMPReader()")
        self.readerName = "_bmpReader"
        
        return

    def load(self, file):
        """
        Loads bmp image data from file.

        @param file: The filename from which to load bmp image data
        """
        if _debug: print "\t%s: Called BmpImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# BmpImage.load()")
        evalString = "_bmpReader.SetFileName(\"%s\")" % file
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does BmpImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called BmpImage.render()" % rendererName

        self.renderer.addToEvalStack("# BmpImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_bmpReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return

class TiffImage(Image):
    """
    Subclass of Image class to explicitly handle tiff images
    """
    def __init__(self, scene):
        """
        Initialises the TiffImage class object

        @param scene: The Scene object to add to
        @type scene: scene object
        """
        if _debug: print "\t%s: Called TiffImage.__init__()" % rendererName
        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# TiffImage.__init__()")
        self.renderer.addToEvalStack("_tiffReader = vtk.vtkTIFFReader()")
        self.readerName = "_tiffReader"
        
        return

    def load(self, file):
        """
        Loads tiff image data from file.

        @param file: The filename from which to load tiff image data
        """
        if _debug: print "\t%s: Called TiffImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# TiffImage.load()")
        evalString = "_tiffReader.SetFileName(\"%s\")" % file
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does TiffImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called TiffImage.render()" % rendererName

        self.renderer.addToEvalStack("# TiffImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_tiffReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return

class PnmImage(Image):
    """
    Subclass of Image class to explicitly handle pnm (ppm, pgm, pbm) images
    """
    def __init__(self, scene):
        """
        Initialises the PnmImage class object

        @param scene: The Scene object to add to
        @type scene: scene object
        """
        if _debug: print "\t%s: Called PnmImage.__init__()" % rendererName
        self.renderer = scene.renderer
        self.renderer.addToEvalStack("# PnmImage.__init__()")
        self.renderer.addToEvalStack("_pnmReader = vtk.vtkPNMReader()")
        self.readerName = "_pnmReader"
        
        return

    def load(self, file):
        """
        Loads pnm (ppm, pgm, pbm) image data from file.

        @param file: The filename from which to load pnm image data
        """
        if _debug: print "\t%s: Called PnmImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# PnmImage.load()")
        evalString = "_pnmReader.SetFileName(\"%s\")" % file
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does PnmImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called PnmImage.render()" % rendererName

        self.renderer.addToEvalStack("# PnmImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_pnmReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return



# vim: expandtab shiftwidth=4:
