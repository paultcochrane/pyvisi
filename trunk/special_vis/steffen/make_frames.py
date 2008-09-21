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

vertical_cut_height = 0.0
elevation_angle = 0.0
view_radius = 70
for i in xrange(numframes):
    os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -n %i -v %g -e %g -r %g" %
    (i,i,numframes,vertical_cut_height,elevation_angle,view_radius))
