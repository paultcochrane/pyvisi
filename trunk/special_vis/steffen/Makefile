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
	python make_frames_loop.py

annotate:
	perl image_annotate.pl -t $(SIMTAG)

ppm: annotate
	for file in `ls -1 frame_*_ann.tga`; \
	do \
	tgatoppm $$file > $$file.ppm; \
	done

movie: annotate
	mencoder mf://*_ann.tga -mf w=800:h=600:fps=25:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -ovc raw -o $(SIMTAG)_povray.avi
	#ppmtompeg $(SIMTAG)_povray_ann.params

clean:
	rm frame_*_ann.tga
