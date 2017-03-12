from music21 import *

lowerBound = 24
upperBound = 102

def getMidiFile(fileName):
	mf = midi.MidiFile()
	mf.open(fileName)
	mf.read()
	mf.close()
	return mf
	
def readFile(fileName):
	#read file contents into MidiFile object mf
	mf = getMidiFile(fileName)
	timeLeft = [track.events[0].time for track in mf.tracks]
	posns = [0 for track in mf.tracks]

	time = 0
	span = upperBound - lowerBound

	stateMatrix = []
	state = [[0,0] for x in range(span)]
	stateMatrix.append(state)
	
	#resolution of midi file
	res = mf.ticksPerQuarterNote	

	while True:
		#crossed a note boundary; create new state
		if time % (res/4) == res/16:
			oldState = state
			state = [[oldState[x][0],0] for x in range(span)]
			stateMatrix.append(state)

		for i in range(len(timeLeft)):
			while timeLeft[i] == 0:
				track = mf.tracks[i]
				pos = posns[i]

				ev = track.events[pos+1]
				tev = ev.type
				if tev == 'NOTE_ON':
					if ev.pitch < lowerBound or ev.pitch >= upperBound:
						pass
					else:
						if ev.velocity == 0:
							state[ev.pitch-lowerBound] = [0,0]
						else:
							state[ev.pitch-lowerBound] = [1,1]
				try:
					timeLeft[i] = track.events[pos+2].time
					posns[i] += 2
				except IndexError:
					timeLeft[i] = None
			
			if timeLeft[i] is not None:
				timeLeft[i] -= 1

		if all(t is None for t in timeLeft):
			break

		time += 1
	
	return stateMatrix

def writeFile(stateMatrix, name="example"):
	stateMatrix = numpy.asarray(stateMatrix)
#print(readFile('br_im2.mid'))
