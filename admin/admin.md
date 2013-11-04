Admin tasks
===========

Epydoc
------

Epydoc is used to build the API documentation of pyvisi.  It strips out
relevant information from the python code and the docstrings in the python
code to generate a set of web pages documenting the different classes and
functions defined.

The command used to run epydoc is:

    epydoc --html -o doc/api_epydoc -n pyvisi pyvisi

Pylint
------

Pylint is a handy tool to check the quality of the code.  It is like the old
lint program for C, and gives a lot of checking and helpful output.  To
generate html output from pylint use the following command from the pyvisi
main directory:

    pylint --output-format=html --rcfile=.pylintrc pyvisi > pylint.pyvisi.html
