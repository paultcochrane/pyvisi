# $Id$

.PHONY: clean annotate movie

frames:
	os.system("python make_frame_povray.py -d vtk -f frame_%i.vtu -i %i -o vtk -n 201" % (i,i))

annotate:
	perl image_annotate.pl -t S003

ppm: annotate
	for file in `ls -1 frame_*_ann.tga`; \
	do \
	tgatoppm $$file > $$file.ppm; \
	done

movie: annotate
	mencoder mf://*_ann.tga -mf w=800:h=600:fps=25:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -ovc raw -o S003_povray.avi
	#ppmtompeg S003_povray_ann.params

clean:
	rm frame_*_ann.tga
