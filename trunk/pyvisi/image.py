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

from common import _debug, overrideWarning
import inspect
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
        if _debug: print "\tBASE: Called Image.__init__()"

        if format == "jpeg":
            if _debug: print "\tBASE: Using jpeg image format"
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
        if _debug: print "\tBASE: Called Image.load()"

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
        if _debug: print "\tBASE: Called JpegImage.__init__()"
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads jpeg image data from file.

        @param file: The filename from which to load jpeg image data
        @type file: string
        """
        if _debug: print "\tBASE: Called JpegImage.load()"

        # print a warning message if get to here
        overrideWarning("JpegImage.load")

        return

    def render(self):
        """
        Does JpegImage object specific (pre)rendering stuff
        """
        if _debug: print "\tBASE: Called JpegImage.render()"

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
        if _debug: print "\tBASE: Called PngImage.__init__()"
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads png image data from file.

        @param file: The filename from which to load png image data
        @type file: string
        """
        if _debug: print "\tBASE: Called PngImage.load()"

        # print a warning message if get to here
        overrideWarning("PngImage.load")

        return

    def render(self):
        """
        Does PngImage object specific (pre)rendering stuff
        """
        if _debug: print "\tBASE: Called PngImage.render()"

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
        if _debug: print "\tBASE: Called BmpImage.__init__()"
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads bmp image data from file.

        @param file: The filename from which to load bmp image data
        @type file: string
        """
        if _debug: print "\tBASE: Called BmpImage.load()"

        # print a warning message if get to here
        overrideWarning("BmpImage.load")

        return

    def render(self):
        """
        Does BmpImage object specific (pre)rendering stuff
        """
        if _debug: print "\tBASE: Called BmpImage.render()"

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
        if _debug: print "\tBASE: Called TiffImage.__init__()"
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads tiff image data from file.

        @param file: The filename from which to load tiff image data
        @type file: string
        """
        if _debug: print "\tBASE: Called TiffImage.load()"

        # print a warning message if get to here
        overrideWarning("TiffImage.load")

        return

    def render(self):
        """
        Does TiffImage object specific (pre)rendering stuff
        """
        if _debug: print "\tBASE: Called TiffImage.render()"

        # print a warning message if get to here
        overrideWarning("TiffImage.render")

        return



# vim: expandtab shiftwidth=4:
