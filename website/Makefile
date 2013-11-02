# main html files

.PHONY: clean date_updated.part todo examples
.SUFFIXES: .html

FILES = \
	index.html\
	docs.html\
	devel.html\
	examples.html\
	news.html\
	contacts.html\
	links.html\
	renderers.html\
	support.html\
	todo.html

PART_FILES = \
	contacts/*.part\
	devel/*.part\
	docs/*.part\
	examples/*.part\
	htmlbuild/*.part\
	index/*.part\
	links/*.part\
	news/*.part\
	renderers/*.part\
	support/*.part\
	todo/*.part

# helper part files for building the html
PARTS_DIR = htmlbuild

# where the css files are kept
CSS_DIR = css

# the manual directory
MANUAL_DIR = docs/manual

# epydoc docs base directory
EPYDOC_DIR = docs/api_epydoc

# the stuff to publish to the website
PUBLISH_FILES = \
	$(FILES)\
	$(CSS_DIR)/pyvisi_banner-o.css\
	$(CSS_DIR)/pyvisi_banner.css\
	$(CSS_DIR)/pyvisi.css\
	images/*.gif\
	images/*.jpg\
	$(EPYDOC_DIR)/*.css\
	$(EPYDOC_DIR)/*.html\
	$(EPYDOC_DIR)/public/*.css\
	$(EPYDOC_DIR)/public/*.html\
	$(EPYDOC_DIR)/private/*.css\
	$(EPYDOC_DIR)/private/*.html\
	$(MANUAL_DIR)/pyvisi_doc.pdf\
	examples/*.png\
	examples/*.html

# generating the html
all: date_updated.part todo examples $(FILES)

# generate the last updated text at the bottom of the page
date_updated.part:
	echo "<td class=\"updated\"><br>" > $@
	echo "<i>Last updated: " >> $@
	date >> $@
	echo "</i><br>" >> $@
	echo "comments to: " >> $@
	echo "<a href=\"mailto:paul@liekut.de">webmaster</a>" >> $@
	echo "<br></td>" >> $@

# dependencies from various .part files
PARTS_DEPS = \
	$(PARTS_DIR)/doctype.part\
	$(PARTS_DIR)/banner.part\
	$(PARTS_DIR)/spacer_start.part\
	$(PARTS_DIR)/spacer_end.part\
	$(PARTS_DIR)/general_footer.part

# hrm, the html getting built doesn't depend on the stuff which is going to
# change the most...  how does one organise this properly?
%.html: $(PARTS_DEPS) $(PART_FILES)
	cat $(PARTS_DIR)/doctype.part > $@
	cat $*/$*_header.part >> $@
	cat $(PARTS_DIR)/banner.part >> $@
	cat $(PARTS_DIR)/spacer_start.part >> $@
	cat $*/$*_body.part >> $@
	cat $(PARTS_DIR)/spacer_end.part >> $@
	cat date_updated.part >> $@
	cat $(PARTS_DIR)/general_footer.part >> $@

todo:
	cd todo; python todoBodyMake.py

examples:
	$(MAKE) --directory examples

clean:
	rm -f $(FILES) date_updated.part
	$(MAKE) --directory examples clean

