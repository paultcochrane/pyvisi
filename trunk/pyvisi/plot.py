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

## @file plot.py

"""
Class and functions associated with a pyvisi Plot objects
"""

from common import _debug

from scene import BaseScene
from item import BaseItem

class BasePlot(BaseScene):
    """
    Abstract plot class
    """
    def __init__(self):
        if _debug: print "\tBASE: Called Plot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in Plot()"
        return True

class BaseArrowPlot(BasePlot):
    """
    Arrow field plot
    """
    def __init__(self):
        if _debug: print "\tBASE: Called ArrowPlot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in ArrowPlot()"
        return True

class BaseContourPlot(BasePlot):
    """
    Contour plot
    """
    def __init__(self):
        if _debug: print "\tBASE: Called ContourPlot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in ContourPlot()"
        return True

class BaseLinePlot(BasePlot):
    """
    Line plot
    """
    def __init__(self):
        if _debug: print "\tBASE: Called LinePlot.__init__()"
        pass

    def setData(self,data):
        if _debug: print "\tBASE: Called setData() in LinePlot()"
        return True

# vim: expandtab shiftwidth=4:

