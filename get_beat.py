#!/usr/bin/python -u
import struct
import sys, time


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
byte = f.read(2)
pos = 0
smoothing  = 1.5
v=0
smaInstant = Simplemovingaverage(700)
smaLocal = Simplemovingaverage(7000)
bpm = 0
start = time.time()
while True:
	if byte == "":
		byte = f.read(2)
	pos += 1
	#v += (struct.unpack('<h', byte)[0] - v) / smoothing
	v = struct.unpack('<h', byte)[0] 

	inst = smaInstant(v)	
	local = smaLocal(v)	
	try:
		if (inst/local) > 30: bpm += 1
	except:
		pass
	byte = f.read(2)

	if pos % 8000 == 0:
		print 'fps: ', (8000 / (time.time() - start))
		print 'bpm', bpm
		bpm = 0
		start = time.time()

