#!/usr/bin/env python
'''
CREATED:2014-06-04 11:43:30 by Colin Raffel <craffel@gmail.com>

Detect onsets in an audio file

Usage:   ./onset_detector.py [-h] input_file.mp3    output_onsets.csv
'''
from __future__ import print_function

import sys
import librosa
import argparse
import time 
import vlc


def onset_detect(input_file, output_csv):
    '''Onset detection function

    :parameters:
      - input_file : str
          Path to input audio file (wav, mp3, m4a, flac, etc.)

      - output_file : str
          Path to save onset timestamps as a CSV file
    '''
    p = vlc.MediaPlayer(input_file)

    # 1. load the wav file and resample to 22.050 KHz
   # print('Loading ', input_file)
    y, sr = librosa.load(input_file, sr=22050)

    # Use a default hop size of 512 frames @ 22KHz ~= 23ms
    hop_length = 512

    # This is the window length used by default in stft
    n_fft = 2048

    # 2. run onset detection
#    print('Detecting onsets...')
    onsets = librosa.onset.onset_detect(y=y,
                                        sr=sr,
                                        hop_length=hop_length)

#    print("Found {:d} onsets.".format(onsets.shape[0]))

    # 3. save outputx
    # 'beats' will contain the frame numbers of beat events.

    onset_times = librosa.frames_to_time(onsets,
                                         sr=sr,
                                         hop_length=hop_length,
                                         n_fft=n_fft)

    i, t = 1, 0 
    start = time.clock()
    delta = []
    delta1 = []
    delta2 = []
    delta3 = []
    delta4 = []
    delta5 = []

    for i in range (1, len(onset_times)):
        delta.append(onset_times[i] - onset_times[i-1])

    for i in range (0, len(delta)):
        if (i<4): 
            num = 0
            for x in range(0, i+1):
                num += delta[x]
            delta1.append(num)
        else: 
            delta1.append(delta[i] + delta[i-1] + delta[i-2] + delta[i-3] + delta[i-4])


    for i in range (0, len(delta1)):
        if (i<4): 
            num = 0
            for x in range(0, i+1):
                num += delta1[x]
            delta2.append(num)
        else: 
            delta2.append(delta1[i] + delta1[i-1] + delta1[i-2] + delta1[i-3] + delta1[i-4])

    
    for i in range (0, len(delta2)):
        if (i<4): 
            num = 0
            for x in range(0, i+1):
                num += delta2[x]
            delta3.append(num)
        else: 
            delta3.append(delta2[i] + delta2[i-1] + delta2[i-2] + delta2[i-3] + delta2[i-4])    

    for i in range (0, len(delta3)):
        if (i<4): 
            num = 0
            for x in range(0, i+1):
                num += delta3[x]
            delta4.append(num)
        else: 
            delta4.append(delta3[i] + delta3[i-1] + delta3[i-2] + delta3[i-3] + delta3[i-4])    

    for i in range (0, len(delta4)):
        if (i<4): 
            num = 0
            for x in range(0, i+1):
                num += delta3[x]
            delta5.append(num)
        else: 
            delta5.append(delta4[i] + delta4[i-1] + delta4[i-2] + delta4[i-3] + delta4[i-4])   






    librosa.output.times_csv(output_csv, onset_times)



    for aslt in delta5:
        print (aslt)



def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(
        description='librosa onset detection example')

    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')

    parser.add_argument('output_file',
                        action='store',
                        help='path to the output file (csv of onset times)')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # Get the parameters
    parameters = process_arguments(sys.argv[1:])

    # Run the beat tracker
    onset_detect(parameters['input_file'], parameters['output_file'])
