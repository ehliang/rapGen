# Beat tracking example
from __future__ import print_function
import numpy as np
import librosa
import time
import vlc

filename = './rap2.mp3' 

y, sr = librosa.load(filename)
p = vlc.MediaPlayer(filename)




		
y_harmonic, y_percussive = librosa.effects.hpss(y)

tempo, beat_frames = librosa.beat.beat_track(y=y_percussive,sr=sr)
tempo, beat_frames2 = librosa.beat.beat_track(y=y_harmonic,sr=sr)

mfcc = librosa.feature.mfcc(y=y, sr=sr, hop_length=512, n_mfcc=13)


mfcc_delta = librosa.feature.delta(mfcc)


beat_mfcc_delta = librosa.feature.sync(np.vstack([mfcc, mfcc_delta]),
                                       beat_frames)


beat_times = librosa.frames_to_time(beat_frames, sr=sr)
beat_times2 = librosa.frames_to_time(beat_frames2, sr=sr)
i, t = 0, 0 
start = time.clock()
p.play()
while (i<min(len(beat_times), len(beat_times2))):
	if ((time.clock()-start) >= beat_times[i]):
		i+=1
		print('beat', i)
	if ((time.clock()-start) >= beat_times[t]):
		t+=1
		print('harmonic', t)
print('Saving output to beat_times.csv')
librosa.output.times_csv('beat_times.csv', beat_times)
