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

Base implementation.
"""

# generic import
from pyvisi.common import debugMsg, overrideWarning, unsupportedError, fileCheck

from pyvisi.item import Item

__revision__ = 'pre-alpha-1'

class Image(Item):
    """
    Image class.  Generic class to handle image data.
    """
    def __init__(self, format, scene):
        """
        Initialises the Image class object
        
        @param format: The image format
        @type format: string

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Item.__init__(self)
        debugMsg("Called Image.__init__()")

        if format is None:
            raise ValueError, "You must specify a format"

        if scene is None:
            raise ValueError, "You must specify a scene"

        #if format == "jpeg":
            #debugMsg("Using jpeg image format")
            #return JpegImage(scene)
        #else:
            #print "Unknown image format %s" % format
            #return None

    def load(self, fname):
        """
        Loads image data from file.

        @param fname: The filename from which to load image data
        @type fname: string
        """
        debugMsg("Called Image.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("Image.load")

        return

class JpegImage(Image):
    """
    Subclass of Image class to explicitly handle jpeg images
    """
    def __init__(self, scene):
        """
        Initialises the JpegImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called JpegImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads jpeg image data from file.

        @param fname: The filename from which to load jpeg image data
        @type fname: string
        """
        debugMsg("Called JpegImage.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("JpegImage.load")

        return

    def render(self):
        """
        Does JpegImage object specific (pre)rendering stuff
        """
        debugMsg("Called JpegImage.render()")

        # print a warning message if get to here
        overrideWarning("JpegImage.render")

        return

class PngImage(Image):
    """
    Subclass of Image class to explicitly handle png images
    """
    def __init__(self, scene):
        """
        Initialises the PngImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PngImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads png image data from file.

        @param fname: The filename from which to load png image data
        @type fname: string
        """
        debugMsg("Called PngImage.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("PngImage.load")

        return

    def render(self):
        """
        Does PngImage object specific (pre)rendering stuff
        """
        debugMsg("Called PngImage.render()")

        # print a warning message if get to here
        overrideWarning("PngImage.render")

        return

class BmpImage(Image):
    """
    Subclass of Image class to explicitly handle bmp images
    """
    def __init__(self, scene):
        """
        Initialises the BmpImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called BmpImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads bmp image data from file.

        @param fname: The filename from which to load bmp image data
        @type fname: string
        """
        debugMsg("Called BmpImage.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("BmpImage.load")

        return

    def render(self):
        """
        Does BmpImage object specific (pre)rendering stuff
        """
        debugMsg("Called BmpImage.render()")

        # print a warning message if get to here
        overrideWarning("BmpImage.render")

        return

class TiffImage(Image):
    """
    Subclass of Image class to explicitly handle tiff images
    """
    def __init__(self, scene):
        """
        Initialises the TiffImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called TiffImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads tiff image data from file.

        @param fname: The filename from which to load tiff image data
        @type fname: string
        """
        debugMsg("Called TiffImage.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("TiffImage.load")

        return

    def render(self):
        """
        Does TiffImage object specific (pre)rendering stuff
        """
        debugMsg("Called TiffImage.render()")

        # print a warning message if get to here
        overrideWarning("TiffImage.render")

        return

class PnmImage(Image):
    """
    Subclass of Image class to explicitly handle pnm images
    """
    def __init__(self, scene):
        """
        Initialises the PnmImage class object

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PnmImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads pnm image data from file.

        @param fname: The filename from which to load pnm image data
        @type fname: string
        """
        debugMsg("Called PnmImage.load()")

        # do a check to see if the file exists
        fileCheck(fname)

        # print a warning message if get to here
        overrideWarning("PnmImage.load")

        return

    def render(self):
        """
        Does PnmImage object specific (pre)rendering stuff
        """
        debugMsg("Called PnmImage.render()")

        # print a warning message if get to here
        overrideWarning("PnmImage.render")

        return

class PsImage(Image):
    """
    Subclass of Image class to explicitly handle ps images
    """
    def __init__(self, scene):
        """
        Initialises the PsImage class object

        This object is B{only} used for generating postscript output

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PsImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads ps image data from file.

        B{NOT} supported by this renderer module

        @param fname: The filename from which to load ps image data
        @type fname: string
        """
        debugMsg("Called PsImage.load()")

        # this ability not handled by this renderer module
        unsupportedError("BASE")
        
        # do a check to see if the file exists
        fileCheck(fname)

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
    def __init__(self, scene):
        """
        Initialises the PdfImage class object

        This object is B{only} used for generating pdf output

        @param scene: The Scene object to add to
        @type scene: Scene object
        """
        Image.__init__(self)
        debugMsg("Called PdfImage.__init__()")
        self.renderer = scene.renderer

    def load(self, fname):
        """
        Loads pdf image data from file.

        B{NOT} supported by this renderer module

        @param fname: The filename from which to load pdf image data
        @type fname: string
        """
        debugMsg("Called PdfImage.load()")

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script

        # this ability not handled by this renderer module
        unsupportedError("BASE")
        
        # do a check to see if the file exists
        fileCheck(fname)

        return

    def render(self):
        """
        Does PdfImage object specific (pre)rendering stuff
        """
        debugMsg("Called PdfImage.render()")

        return

# vim: expandtab shiftwidth=4:
