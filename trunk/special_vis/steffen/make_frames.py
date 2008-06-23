#!/usr/bin/env python

import os


for i in xrange(201):
    os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -n 201 -v 8" % (i,i))
