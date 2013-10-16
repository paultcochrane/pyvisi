# example html files
# $Id$

.PHONY: clean copy
.SUFFIXES: .html .py

FILES = \
	arrowPlot.html\
	arrowPlot2D.html\
	arrowPlot3D.html\
	ballPlot.html\
	contourPlot.html\
	contourPlotMovie.html\
	isosurfacePlot.html\
	meshPlot.html\
	multiCurveLinePlot.html\
	offsetLinePlot.html\
	offsetPlot.html\
	seismicOffsetPlot1.html\
	seismicOffsetPlot2.html\
	seismicOffsetPlot3.html\
	simpleLinePlot.html\
	simpleLinePlotMovie.html\
	singleArrayLinePlot.html\
	surfaceAndContourPlot.html\
	surfacePlot.html\
	scatterPlot.html\
	scatterPlot3D.html

EXAMPLES_DIR = ../../examples

PYTHON_FILES = \
	arrowPlot.py\
	arrowPlot2D.py\
	arrowPlot3D.py\
	ballPlot.py\
	contourPlot.py\
	contourPlotMovie.py\
	isosurfacePlot.py\
	multiCurveLinePlot.py\
	meshPlot.py\
	offsetLinePlot.py\
	offsetPlot.py\
	seismicOffsetPlot1.py\
	seismicOffsetPlot2.py\
	seismicOffsetPlot3.py\
	simpleLinePlot.py\
	simpleLinePlotMovie.py\
	singleArrayLinePlot.py\
	surfaceAndContourPlot.py\
	surfacePlot.py\
	scatterPlot.py\
	scatterPlot3D.py

# generating the source
all: $(PYTHON_FILES) $(FILES)

%.py:
	cp $(EXAMPLES_DIR)/$*.py .

%.html: $(PYTHON_FILES)
	enscript -Epython --lang=html --color -o $@ --title=$*.py $*.py
	rm $*.py

clean:
	rm -f $(FILES) $(PYTHON_FILES)
