#!/usr/bin/env python

# $Id$

import xml.dom.minidom
import re

headString = '''
<!-- $Id$ -->
  <h1>Todo list</h1>
  
  <hr class="top" />

'''

# open the todo file
f = open('../../.todo','r')

# parse the document
doc = xml.dom.minidom.parse(f)

# close the todo file (like a good little boy)
f.close()

# grab all of the <note> elements
notes = doc.getElementsByTagName('note')

# regular expression objects for the whitespace at the start and end
# of strings respectively
r1 = re.compile(r'^\s+')
r2 = re.compile(r'\s+$')

# the html string object for the 'done' items
doneHtml = '''
<h2>Completed todo items</h2>
<table class="todo">
  <tr>
    <th>Task description</th>
    <th>Date added</th>
    <th>Date completed</th>
    <th>Comment</th>
  </tr>
'''

# the html string for the 'todo' items
todoHtml = '''
<h2>Todo items</h2>
<table class="todo">
  <tr>
    <th>Task description</th>
    <th>Date added</th>
    <th>Priority</th>
  </tr>
'''

for note in notes:
    # if the thing is done, store what it was, when it was finished, 
    # and the comment
    if note.hasAttribute('done'):
	# grab the attributes
	startTime = note.getAttribute('time')
	doneTime = note.getAttribute('done')
	priority = note.getAttribute('priority')
	# grab the note text
	noteText = note.firstChild.nodeValue
	noteText = r1.sub('',noteText)
	noteText = r2.sub('',noteText)
	# grab the comment text
	comments = note.getElementsByTagName('comment')
	commentNode = comments[0]
	commentText = commentNode.firstChild.nodeValue
	commentText = r1.sub('',commentText)
	commentText = r2.sub('',commentText)

	# now generate the html for 'done' items
	doneHtml += "<tr class=\"done\">\n"
	doneHtml += "  <td>%s</td>\n" % noteText
	doneHtml += "  <td>%s</td>\n" % startTime
	doneHtml += "  <td>%s</td>\n" % doneTime
	doneHtml += "  <td>%s</td>\n" % commentText
	doneHtml += "</tr>\n"

    else:
	# grab the attributes
	startTime = note.getAttribute('time')
	priority = note.getAttribute('priority')
	# grab the note text
	noteText = note.firstChild.nodeValue
	noteText = r1.sub('',noteText)
	noteText = r2.sub('',noteText)
	
	# now generate the html for the 'todo' items
	todoHtml += "<tr class=\"%s\">\n" % priority
	todoHtml += "  <td>%s</td>\n" % noteText
	todoHtml += "  <td>%s</td>\n" % startTime
	todoHtml += "  <td>%s</td>\n" % priority
	todoHtml += "</tr>\n"

# finish off the html elements
doneHtml += "</table>\n"
todoHtml += "</table>\n"

# generate the html string to print
todoBodyPartHtml = headString + todoHtml + doneHtml

# write the html to file
f = open("todo_body.part","w")
f.write(todoBodyPartHtml)
f.close()


