# $Id$

.PHONY: clean annotate movie config

SIMTAG = $(notdir $(CURDIR))
ifeq "$(SIMTAG)" ""
    $(error "Could not determine SIMTAG from CURDIR")
endif


config:
	python config.py

frames:
	@echo "Building frames for $(SIMTAG)"
	NUM_FRAMES=`ls -1 vtk/*.vtu | wc -l`;\
	python make_frames.py --numframes=$$NUM_FRAMES

frames_loop: config
	@echo "Building frames to loop for $(SIMTAG)"
	NUM_FRAMES=`ls -1 vtk/*.vtu | wc -l`;\
	python make_frames_loop.py --numframes=$$NUM_FRAMES

annotate: frames
	NUM_FRAMES=`ls -1 vtk/*.vtu | wc -l`;\
	perl image_annotate.pl -t $(SIMTAG) -m $$NUM_FRAMES

annotate_loop: frames_loop
	NUM_FRAMES=`ls -1 vtk/*.vtu | wc -l`;\
	NUM_FRAMES=`expr $$NUM_FRAMES * 2`;\
	NUM_FRAMES=`expr $$NUM_FRAMES + 1`;\
	perl image_annotate.pl -t $(SIMTAG) -m $$NUM_FRAMES -s frame_loop

ppm: annotate
	for file in `ls -1 frame_*_ann.tga`; \
	do \
	tgatoppm $$file > $$file.ppm; \
	done

#MENCODER_OPTS = -mf w=800:h=600:fps=25:type=tga -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -ovc raw
MENCODER_OPTS = -mf w=800:h=600:fps=25:type=tga -o bar.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000:vpass=1
MENCODER_OPTS2 = -mf w=800:h=600:fps=25:type=tga -o bar.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000:vpass=2

movie: annotate
	mencoder mf://frame_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS) -o $(SIMTAG)_povray.avi
	mencoder mf://frame_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS2) -o $(SIMTAG)_povray.avi
	#ppmtompeg $(SIMTAG)_povray_ann.params

movie_zip:
	bzip2 -9 $(SIMTAG)_povray.avi

movie_loop: annotate_loop
	mencoder mf://frame_loop_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS) -o $(SIMTAG)_loop_povray.avi
	mencoder mf://frame_loop_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS2) -o $(SIMTAG)_loop_povray.avi

movie_loop_zip:
	bzip2 -9 $(SIMTAG)_loop_povray.avi

clean:
	rm -f frame_*.tga $(SIMTAG)_povray.avi $(SIMTAG)_loop_povray.avi $(SIMTAG)_povray.avi.bz2 $(SIMTAG)_loop_povray.avi.bz2 divx2pass.log
