#!/usr/bin/env python

import os

for i in xrange(401):
    if i > 200:
	index = 400 - i
	os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -s frame_loop -n 201 -v 8" % (index,i))
    else:
	os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -s frame_loop -n 201 -v 8" % (i,i))
