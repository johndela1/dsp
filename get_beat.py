#!/usr/bin/python -u
import struct
import sys, time

def expDecay(newValue, workingAverage, smoothingFactor):
	return (newValue*smoothingFactor) + ( workingAverage * ( 1.0 - smoothingFactor))
	
f = sys.stdin
#f = open('beats.wav')
byte = f.read(2)
pos = 0
v=0
bpm = 0
inst = 0
local = 0
decay = 0
start = time.time()
while byte != "":
	pos += 1
	#v += (struct.unpack('<h', byte)[0] - v) / smoothing
	v = abs(struct.unpack('<h', byte)[0])

	inst = expDecay(v, inst, .01)
	local = expDecay(v, local, .001)
	try:
		if (inst/float(local)) > 2 and decay <= 0:
			bpm += 1
			print '------beat-----'
			decay = 3000
	except:
		pass
	decay -= 1
	byte = f.read(2)

	if pos % 32000 == 0:
		print 'fps: ', (8000 / (time.time() - start))
		print 'bpm', bpm *15
		bpm = 0
		start = time.time()

