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

## @file common.py

"""
Variables common to all classes and functions
"""

_debug = 1
pyvisiVersion = 0.1
pyvisiRevision = 1

def overrideWarning(methodName):
    """
    Print a warning message for functions that need to be overridden but are
    called.

    @param methodName: The method name as a string.
    """
    # print a warning message if get to here
    print "\nWarning!!  If you are reading this message, then the renderer"
    print "           you have chosen hasn't overridden this method as"
    print "           they should have.  Please contact the maintainer of"
    print "           the renderer module, quoting the method name given"
    print "           below, to get this problem fixed."
    print "\nMethod: %s()\n" % methodName

    return

def unsupportedError(rendererName):
    """
    Print an error message when a method is called that is defined in pyvisi
    but is not supported at the renderer module level.

    @param rendererName: the name of the renderer module
    @type rendererName: string
    """
    errorString = "Sorry, but %s doesn't support this method." % rendererName
    raise NotImplementedError(errorString)

    return

# vim: expandtab shiftwidth=4:
