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
        @type format: string

        @param scene: The Scene object to add to
        @type scene: Scene object
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
        @type scene: Scene object
        """
        if _debug: print "\t%s: Called JpegImage.__init__()" % rendererName
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads jpeg image data from file.

        NOT supported by this renderer module

        @param file: The filename from which to load jpeg image data
        @type file: string
        """
        if _debug: print "\t%s: Called JpegImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script

        # this ability not handled by this renderer module
        unsupportedError(rendererName)
        
        return

    def render(self):
        """
        Does JpegImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called JpegImage.render()" % rendererName

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
        if _debug: print "\t%s: Called PngImage.__init__()" % rendererName
        self.renderer = scene.renderer
        
        return

    def load(self, file):
        """
        Loads png image data from file.

        NOT supported by this renderer module

        @param file: The filename from which to load png image data
        @type file: string
        """
        if _debug: print "\t%s: Called PngImage.load()" % rendererName

        # need to check that the file exists and is readable etc here
        # *before* we add to the evalString, better to get the feedback
        # now rather than at the end of the script

        # this ability not handled by this renderer module
        unsupportedError(rendererName)
        
        return

    def render(self):
        """
        Does PngImage object specific (pre)rendering stuff
        """
        if _debug: print "\t%s: Called PngImage.render()" % rendererName

        return

# vim: expandtab shiftwidth=4:
