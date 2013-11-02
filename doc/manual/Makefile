# This is the main file for generating the handcrafted documentation
# for pyvisi.


.PHONY: clean

TEX_FILES = \
	abstract.tex\
        developerManual.tex\
	gpl.tex\
        intro.tex\
        install.tex\
	languageReference.tex\
	misc_defs.tex\
        plottingExamples.tex\
	titlepage.tex\
	tutFromScratch.tex\
	pyvisi_defs.tex\
	pyvisi_doc.tex\
        pyvisi_doc.bib

PDF_FIGS = \
	figures/plotExampleGnuplot.pdf\
        figures/plotExampleVTK.pdf\
        figures/pyvisi_class_structure.pdf

# generating the handcrafted docs
all: pdf

pdf: $(PDF_FIGS) $(TEX_FILES)
	pdflatex pyvisi_doc.tex
	bibtex pyvisi_doc
	makeindex pyvisi_doc
	pdflatex pyvisi_doc.tex
	pdflatex pyvisi_doc.tex

clean:
	rm -f $(PDF_FIGS) *.aux *.bbl *.blg *.idx *.ilg *.ind *.log pyvisi_doc.pdf

