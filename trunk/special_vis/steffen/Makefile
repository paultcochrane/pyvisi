# $Id$

.PHONY: clean annotate movie

frames:
	python make_frames.py

frames_loop:
	python make_frames_loop.py

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
