# Copyright (C) 2004-2008 Paul Cochrane
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


"""
This file contains all of the classes for the various plotting objects.
"""

from pyvisi.renderers.plplot.common import debugMsg

from pyvisi.renderers.plplot.plot import Plot

__revision__ = '$Revision$'

class ArrowPlot(Plot):
    """
    Brief introduction to what the class does
    """

    def __init__(self, arg):
        """
        Initialise arrow plot object
        """
        debugMsg("Called ArrowPlot.__init__()")
        Plot.__init__(self)  # initialisation of base class
 
# vim: expandtab shiftwidth=4:
