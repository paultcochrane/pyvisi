#!/usr/bin/env python

# $Id$

from distutils.core import setup

a=setup(name="pyvisi",
      version="0.1-pre-alpha-2",
      description="The Python Visualisation Interface",
      author="Paul Cochrane",
      author_email="cochrane@esscc.uq.edu.au",
      url="http://pyvisi.sourceforge.net",
      packages=['pyvisi',
      'pyvisi.renderers',
      'pyvisi.renderers.gnuplot',
      'pyvisi.renderers.vtk',
      ],
)


