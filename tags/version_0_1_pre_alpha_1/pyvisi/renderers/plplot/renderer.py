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

## @file renderer.py

"""
Brief introduction to what the file contains/does
"""

from pyvisi.renderers.plplot.common import debugMsg

from pyvisi.renderer import Renderer as BaseRenderer

__revision__ = '$Revision$'

    
class Renderer(BaseRenderer):
    """
    Brief introduction to what the class does
    """

    def __init__(self, arg):
        """
        Brief description of the init function

        @param arg: a description of the argument
        @type arg: the type of the argument
        """
        BaseRenderer.__init__(self)  # initialisation of base class
        debugMsg("Called Renderer.__init__()")
    
    def myfunc(myarg):
        """
        Brief description of what the function does
    
        Replace the text given here with an actual description of what
        the function does.  Also change the name of the function and
        the name of the argument.
    
        @param myarg: Description of what the parameter means/does
        @type myarg: the type of the argument
        """
        return

    
# vim: expandtab shiftwidth=4: