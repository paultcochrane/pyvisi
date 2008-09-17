#!/usr/bin/env python

import os,sys
import getopt
(opts, args) = getopt.getopt(sys.argv[1:],
	"n:",
	[
	"numframes=", 
	],
	)

numframes = None
for option, arg in opts:
    if option in ('-n', '--numframes'):
	numframes = int(arg)

if numframes is None:
    raise ValueError, "You must supply the maximum number of frames"

totalframes = numframes*2 - 1
for i in xrange(totalframes):
    if i > numframes-1:
	index = totalframes - 1 - i
	os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -s frame_loop -n %i -v 8 -e -75 -r 70" % (index,i,numframes))
    else:
	os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -s frame_loop -n %i -v 8 -e -75 -r 70" % (i,i,numframes))
