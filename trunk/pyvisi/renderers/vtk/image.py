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
from pyvisi.renderers.vtk.common \
        import debugMsg, unsupportedError

from pyvisi.common import fileCheck

# module specific imports
from pyvisi.renderers.vtk.item import Item

__revision__ = 'pre-alpha-1'

class Image(Item):
    """
    Image class.  Generic class to handle image data.
    """
    def __init__(self, scene=None):
        """
        Initialises the Image class object
        
        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Item.__init__(self)
        debugMsg("Called Image.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
        
    def load(self, fname):
        """
        Loads image data from file.

        @param fname: The filename from which to load image data
        @type fname: string
        """
        debugMsg("Called Image.load()")

        fileCheck(fname)

        return

class JpegImage(Image):
    """
    Subclass of Image class to explicitly handle jpeg images
    """
    def __init__(self, scene=None):
        """
        Initialises the JpegImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called JpegImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
            self.renderer.addToEvalStack("# JpegImage.__init__()")
            self.renderer.addToEvalStack("_jpegReader = vtk.vtkJPEGReader()")
            self.readerName = "_jpegReader"

        self.format = "jpeg"

    def load(self, fname):
        """
        Loads jpeg image data from file.

        @param fname: The filename from which to load jpeg image data
        @type fname: string
        """
        debugMsg("Called JpegImage.load()")

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script
        
        self.renderer.addToEvalStack("# JpegImage.load()")
        evalString = "_jpegReader.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does JpegImage object specific (pre)rendering stuff
        """
        debugMsg("Called JpegImage.render()")

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
    def __init__(self, scene=None):
        """
        Initialises the PngImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PngImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
            self.renderer.addToEvalStack("# PngImage.__init__()")
            self.renderer.addToEvalStack("_pngReader = vtk.vtkPNGReader()")
            self.readerName = "_pngReader"

        self.format = "png"

    def load(self, fname):
        """
        Loads png image data from file.

        @param fname: The filename from which to load png image data
        @type fname: string
        """
        debugMsg("Called PngImage.load()")

        # check to see if the file exists
        fileCheck(fname)
        
        self.renderer.addToEvalStack("# PngImage.load()")
        evalString = "_pngReader.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does PngImage object specific (pre)rendering stuff
        """
        debugMsg("Called PngImage.render()")

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
    def __init__(self, scene=None):
        """
        Initialises the BmpImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called BmpImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
            self.renderer.addToEvalStack("# BmpImage.__init__()")
            self.renderer.addToEvalStack("_bmpReader = vtk.vtkBMPReader()")
            self.readerName = "_bmpReader"

        self.format = "bmp"

    def load(self, fname):
        """
        Loads bmp image data from file.

        @param fname: The filename from which to load bmp image data
        @type fname: string
        """
        debugMsg("Called BmpImage.load()")

        # check to see if the file exists
        fileCheck(fname)
        
        self.renderer.addToEvalStack("# BmpImage.load()")
        evalString = "_bmpReader.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does BmpImage object specific (pre)rendering stuff
        """
        debugMsg("Called BmpImage.render()")

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
    def __init__(self, scene=None):
        """
        Initialises the TiffImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called TiffImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
            self.renderer.addToEvalStack("# TiffImage.__init__()")
            self.renderer.addToEvalStack("_tiffReader = vtk.vtkTIFFReader()")
            self.readerName = "_tiffReader"

        self.format = "tiff"

    def load(self, fname):
        """
        Loads tiff image data from file.

        @param fname: The filename from which to load tiff image data
        @type fname: string
        """
        debugMsg("Called TiffImage.load()")

        # check to see if the file exists
        fileCheck(fname)

        self.renderer.addToEvalStack("# TiffImage.load()")
        evalString = "_tiffReader.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does TiffImage object specific (pre)rendering stuff
        """
        debugMsg("Called TiffImage.render()")

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
    def __init__(self, scene=None):
        """
        Initialises the PnmImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PnmImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer
            self.renderer.addToEvalStack("# PnmImage.__init__()")
            self.renderer.addToEvalStack("_pnmReader = vtk.vtkPNMReader()")
            self.readerName = "_pnmReader"

        self.format = "pnm"
        
    def load(self, fname):
        """
        Loads pnm (ppm, pgm, pbm) image data from file.

        @param fname: The filename from which to load pnm image data
        @type fname: string
        """
        debugMsg("Called PnmImage.load()")

        # check to see if the file exists
        fileCheck(fname)

        self.renderer.addToEvalStack("# PnmImage.load()")
        evalString = "_pnmReader.SetFileName(\"%s\")" % fname
        self.renderer.addToEvalStack(evalString)
        return

    def render(self):
        """
        Does PnmImage object specific (pre)rendering stuff
        """
        debugMsg("Called PnmImage.render()")

        self.renderer.addToEvalStack("# PnmImage.render()")
        self.renderer.addToEvalStack("_imgActor = vtk.vtkImageActor()")
        self.renderer.addToEvalStack(\
                "_imgActor.SetInput(_pnmReader.GetOutput())")
        self.renderer.addToEvalStack("_renderer.AddActor(_imgActor)")
        return

class PsImage(Image):
    """
    Subclass of Image class to explicitly handle ps images
    """
    def __init__(self, scene=None):
        """
        Initialises the PsImage class object

        This object is B{only} used for generating postscript output

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PsImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer

        self.format = "ps"

    def load(self, fname):
        """
        Loads ps image data from file.

        B{NOT} supported by this renderer module

        @param fname: The filename from which to load ps image data
        @type fname: string
        """
        debugMsg("Called PsImage.load()")

        # need to check if the file exists
        fileCheck(fname)

        # this ability not handled by this renderer module
        unsupportedError()
        
        return

    def render(self):
        """
        Does PsImage object specific (pre)rendering stuff
        """
        debugMsg("Called PsImage.render()")

        return

class PdfImage(Image):
    """
    Subclass of Image class to explicitly handle pdf images
    """
    def __init__(self, scene=None):
        """
        Initialises the PdfImage class object

        This object is B{only} used for generating pdf output

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PdfImage.__init__()")

        if scene is not None:
            self.renderer = scene.renderer

        self.format = "pdf"

    def load(self, fname):
        """
        Loads pdf image data from file.

        B{NOT} supported by this renderer module

        @param fname: The filename from which to load pdf image data
        @type fname: string
        """
        debugMsg("Called PdfImage.load()")

        # need to check that the file exists
        fileCheck(fname)

        # this ability not handled by this renderer module
        unsupportedError()
        
        return

    def render(self):
        """
        Does PdfImage object specific (pre)rendering stuff
        """
        debugMsg("Called PdfImage.render()")

        return

# vim: expandtab shiftwidth=4:
