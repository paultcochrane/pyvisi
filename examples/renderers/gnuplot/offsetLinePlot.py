"""
Example of plotting multiple curves offset from each other

This is especially handy for people plotting seismic data
"""

# set up some data to plot
from Numeric import *

x = arange(0,2*pi,0.01, typecode=Float)
y1 = sin(x)
y2 = cos(x)
y3 = cos(x)**2
y4 = sin(2*x)
y5 = cos(3*x)
y6 = sin(20*x)

#### original gnuplot code

import Gnuplot

# set the plot up
_gnuplot = Gnuplot.Gnuplot()
_gnuplot.title('Example 2D plot with offsets')
_gnuplot.xlabel('x')
_gnuplot.ylabel('y')

### set up the data
# concatenate the data
yAll = concatenate( [y1, y2, y3, y4, y5, y6] )

yMax = max(yAll)
yMin = min(yAll)

# keep the data apart a bit
const = 0.1*(yMax-yMin)

# don't need to worry about y1: it's the first data series
shift = yMax - yMin + const
y2 = y2 + shift
y3 = y3 + 2*shift
y4 = y4 + 3*shift
y5 = y5 + 4*shift
y6 = y6 + 5*shift

_data1 = Gnuplot.Data(x, y1, with='lines')
_data2 = Gnuplot.Data(x, y2, with='lines')
_data3 = Gnuplot.Data(x, y3, with='lines')
_data4 = Gnuplot.Data(x, y4, with='lines')
_data5 = Gnuplot.Data(x, y5, with='lines')
_data6 = Gnuplot.Data(x, y6, with='lines')

# plot it
_gnuplot.plot(_data1, _data2, _data3, _data4, _data5, _data6)

# save it to file
_gnuplot('set terminal png')
_gnuplot('set output "offsetLinePlot.png"')
_gnuplot.plot(_data1, _data2, _data3)

raw_input('Press enter to continue...\n')

# vim: expandtab shiftwidth=4:
