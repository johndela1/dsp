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
smoothing  = 200
sample_rate = 44100
v=0
smaInstant = Simplemovingaverage(100)
smaLocal = Simplemovingaverage(6000)
bpm = 0
while byte != "":
	pos += 1
	v += (struct.unpack('<h', byte)[0] - v) / smoothing
	inst = smaInstant(v)	
	local = smaLocal(v)	
	try:
		if (inst/local) > 900: bpm += 1
	except:
		pass
	byte = f.read(2)
	#trash = f.read(2)

	if pos % 8000 == 0:
		print bpm
		bpm = 0
