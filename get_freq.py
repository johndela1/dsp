#!/usr/bin/python -u
import struct
import sys


from collections import deque
 
class Simplemovingaverage():
    def __init__(self, period):
        assert period == int(period) and period > 0, "Period must be an integer >0"
        self.period = period
        self.stream = deque()
 
    def __call__(self, n):
        stream = self.stream
        stream.append(n)    # appends on the right
        streamlength = len(stream)
        if streamlength > self.period:
            stream.popleft()
            streamlength -= 1
        if streamlength == 0:
            average = 0
        else:
            average = sum( stream ) / streamlength
 
        return average
#f = open('440Hz_44100Hz_16bit_05sec.wav')
f = sys.stdin
#f = open('test.wav')
byte = f.read(2)
#trash = f.read(2)
freq = 0
old_trend = 0
trend = 0
peak = 0
pos = 0
old_v = 0
change = 0
smoothing  = 1
sample_rate = 8000
v=0
while byte != "":
	pos += 1
	v += (struct.unpack('<h', byte)[0] - v) / smoothing
	if old_v < v: trend = 1
	else: trend = -1
	old_v = v
	if old_trend != trend:
		old_trend = trend
		change += 1
	if pos == sample_rate:
		pos = 0
		freq = 	change / 2
		print freq
		change = 0
	byte = f.read(2)
	#trash = f.read(2)

