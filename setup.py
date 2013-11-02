#!/usr/bin/env python

from distutils.core import setup

a=setup(name="pyvisi",
      version="0.1-alpha-1",
      description="The Python Visualisation Interface",
      author="Paul Cochrane",
      author_email="paul@liekut.de",
      url="https://github.com/paultcochrane/pyvisi.git",
      packages=['pyvisi',
      'pyvisi.renderers',
      'pyvisi.renderers.gnuplot',
      'pyvisi.renderers.vtk',
      ],
)
