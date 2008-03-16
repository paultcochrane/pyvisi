# $Id$

.PHONY: clean annotate movie

SIMTAG = $(notdir $(CURDIR))
ifeq "$(SIMTAG)" ""
    $(error "Could not determine SIMTAG from CURDIR")
endif

frames:
	@echo "Building frames for $(SIMTAG)"
	python make_frames.py

frames_loop:
	@echo "Building frames to loop for $(SIMTAG)"
	python make_frames_loop.py

annotate:
	perl image_annotate.pl -t $(SIMTAG)

annotate_loop:
	perl image_annotate.pl -t $(SIMTAG) -m 401 -s frame_loop

ppm: annotate
	for file in `ls -1 frame_*_ann.tga`; \
	do \
	tgatoppm $$file > $$file.ppm; \
	done

movie: annotate
	mencoder mf://*_ann.tga -mf w=800:h=600:fps=25:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -ovc raw -o $(SIMTAG)_povray.avi
	#ppmtompeg $(SIMTAG)_povray_ann.params

movie_loop: annotate_loop
	mencoder mf://frame*loop*_ann.tga -mf w=800:h=600:fps=25:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -ovc raw -o $(SIMTAG)_loop_povray.avi

clean:
	rm frame_*_ann.tga frame_*.tga
