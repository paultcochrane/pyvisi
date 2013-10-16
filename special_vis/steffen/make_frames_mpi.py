#!/usr/bin/env python

from Scientific import MPI
import Numeric, sys
import os

communicator = MPI.world.duplicate()

num_cpus = 4
if communicator.rank == 0:
    for i in xrange(201):
	mod_cpus = i % num_cpus
	print "i = %i, i %% num_cpus = %i" % (i, mod_cpus)
	communicator.send(str(i), mod_cpus, 0)
	#result, source, tag = communicator.receiveString(mod_cpus, None)
	#print result
else:
    index, source, tag = communicator.receiveString(0, None)
    #result = os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -n 201" % (index,index))
    index = int(index)
    print "rank = %i, index = %i" % (communicator.rank, index)
    result = 0
    if result == 0:
	resultStr = "success"
    #communicator.send(resultStr, 0, 42)
