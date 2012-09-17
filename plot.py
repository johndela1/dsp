#!/usr/bin/python
import struct, sys

from pylab import *
import matplotlib.pyplot as plt

f = sys.stdin
y = []
#plt.ion()
#while True:
for i in range(8000):
	y.append(struct.unpack("<h",f.read(2))[0])
y = [int(i) for i in y]
x = [i for i in xrange(8000)]

plot(x,y )

show()
f.close()
