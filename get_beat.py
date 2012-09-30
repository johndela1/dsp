#!/usr/bin/python -u

import struct
import sys, time

def expDecay(newValue, workingAverage, smoothingFactor):
	return ((newValue*smoothingFactor) +
		( workingAverage * ( 1.0 - smoothingFactor)))

	
f = sys.stdin
byte = f.read(2)
pos = 0
v=0
bpm = 0
instEnergy = 0
avgEnergy = 0
decay = 0
start = time.time()
while byte != "":
	pos += 1
	v = abs(struct.unpack('<h', byte)[0])
	#if pos % 10000 == 0: print v
	instEnergy = expDecay(v, instEnergy, .01)
	avgEnergy = expDecay(v, avgEnergy, .001)
	try:
		if (instEnergy/float(avgEnergy)) > 2 and decay <= 0:
			bpm += 1
			print '------beat-----'
			decay = 800
	except:
		pass
	decay -= 1
	byte = f.read(2)

	if False:#pos % 32000 == 0:
		print 'samples/sec:', (32000 / (time.time() - start))
		print 'bpm', bpm *15
		bpm = 0
		start = time.time()

