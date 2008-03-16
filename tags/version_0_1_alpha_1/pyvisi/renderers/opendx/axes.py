# Copyright (C) 2004-2006 Paul Cochrane
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

## @file axes.py

"""
Brief introduction to what the file contains/does
"""

from pyvisi.renderers.opendx.common import debugMsg

from pyvisi.renderers.opendx.plot import Plot

__revision__ = '$Revision$'

    
class Axes(Plot):
    """
    Brief introduction to what the class does
    """

    def __init__(self, arg):
        """
        Brief description of the init function

        @param arg: a description of the argument
        @type arg: the type of the argument
        """
        debugMsg("Called Axes.__init__()")
        Plot.__init__(self)  # initialisation of base class
    
# vim: expandtab shiftwidth=4: