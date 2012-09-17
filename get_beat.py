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
#f = open('beats.wav')
byte = f.read(2)
pos = 0
smoothing  = 1.5
v=0
smaInstant = Simplemovingaverage(500)
smaLocal = Simplemovingaverage(8000)
bpm = 0
decay = 0
start = time.time()
while byte != "":
	pos += 1
	#v += (struct.unpack('<h', byte)[0] - v) / smoothing
	v = abs(struct.unpack('<h', byte)[0])

	inst = smaInstant(v)	
	local = smaLocal(v)	
	if False:# pos % 1000 == 0:
		print 'inst',inst
		print 'local',local
		print 'ratio', inst/local
	try:
		if (inst/float(local)) > 2 and decay <= 0:
			bpm += 1
			print '------beat-----'
			decay = 6000
	except:
		pass
	decay -= 1
	byte = f.read(2)

	if pos % 32000 == 0:
		print 'fps: ', (8000 / (time.time() - start))
		print 'bpm', bpm *15
		bpm = 0
		start = time.time()

