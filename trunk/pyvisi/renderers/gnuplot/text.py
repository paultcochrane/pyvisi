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

## @file text.py

"""
Class and functions associated with a pyvisi Text object
"""

# generic imports
from pyvisi.renderers.gnuplot.common import debugMsg

# module specific imports
from pyvisi.renderers.gnuplot.item import Item

__revision__ = '$Revision$'

class Text(Item):
    """
    Text
    """
    def __init__(self):
        """
        Initialisation of the Text object
        """
        Item.__init__(self)
        debugMsg("Called Text.__init__()")
        self.font = "Times"

    def setFont(self, font):
        """
        Set the current font

        @param font: the font to set
        @type font: string
        """
        self.font = font
        return

    def getFont(self):
        """
        Get the current font
        """
        return self.font

# vim: expandtab shiftwidth=4:
