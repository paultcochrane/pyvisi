# $Id$

.PHONY: clean config padded_vtk

SIMTAG = $(notdir $(CURDIR))
ifeq "$(SIMTAG)" ""
    $(error "Could not determine SIMTAG from CURDIR")
endif

NUM_FRAMES = $(shell ls -1 vtk/*.vtu | wc -l)
NUM_LOOP_FRAMES = $(shell expr expr $(NUM_FRAMES) \* 2 + 1)
LOOP_FRAMES := $(wildcard frame_loop_[0-9][0-9][0-9][0-9].tga)
VTU := $(wildcard vtk/frame_*.vtu)
FRAME_INDICES := $(subst frame_,,$(basename $(notdir $(VTU))))
FRAMES := $(foreach index,$(FRAME_INDICES),$(shell perl -e 'printf "frame_%04d.tga", $(index)'))

config:
	python config.py

padded_vtk:
	for file in `ls -1 vtk/*.vtu`; \
	do \
	frame_index=`echo $$file | sed 's/[^0-9]//g'`; \
	newfile=`perl -e "printf 'vtk/frame_%04d.vtk', $$frame_index"`; \
	echo $$newfile; \
	cp --update $$file $$newfile; \
	done

frames: padded_vtk $(FRAMES)

$(FRAMES): frame_%.tga: vtk/frame_%.vtk
	@echo "Building frames for $(SIMTAG)"
	FRAME_INDEX=`echo $< | sed 's/[^0-9]//g'`; \
	python make_frame_povray.py -d vtk -f frame_$$FRAME_INDEX.vtk -i $$FRAME_INDEX -o vtk -n $(NUM_FRAMES) -v 0 -e 0 -r 100

frames_loop: config
	@echo "Building frames to loop for $(SIMTAG)"
	python make_frames_loop.py --numframes=$(NUM_FRAMES)

annotate: frames
	perl image_annotate.pl -t $(SIMTAG) -m $(NUM_FRAMES)

annotate_loop: frames_loop
	perl image_annotate.pl -t $(SIMTAG) -m $(NUM_LOOP_FRAMES) -s frame_loop

MENCODER_OPTS = -mf w=800:h=600:fps=25:type=tga -o bar.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000:vpass=1
MENCODER_OPTS2 = -mf w=800:h=600:fps=25:type=tga -o bar.avi -ovc lavc -lavcopts vcodec=mpeg4:vbitrate=8000:vpass=2

movie: annotate
	mencoder mf://frame_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS) -o $(SIMTAG)_povray.avi
	mencoder mf://frame_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS2) -o $(SIMTAG)_povray.avi

movie_loop: annotate_loop
	mencoder mf://frame_loop_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS) -o $(SIMTAG)_loop_povray.avi
	mencoder mf://frame_loop_[0-9][0-9][0-9][0-9]_ann.tga $(MENCODER_OPTS2) -o $(SIMTAG)_loop_povray.avi

clean:
	rm -f frame_*.tga $(SIMTAG)_povray.avi $(SIMTAG)_loop_povray.avi $(SIMTAG)_povray.avi.bz2 $(SIMTAG)_loop_povray.avi.bz2 divx2pass.log
