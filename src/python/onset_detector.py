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
import os

def query_rhyme(query, mylist, phrase_array):
    set1 = query(mylist[0], mylist[1])
    set2 = query(mylist[2], mylist[3])

    i, t = 0, 0

    for index in mylist[4]:
        if (index):
            phrase_array.append(set1[i])
            i+=1
        else:
            phrase_array.append(set2[t])
            t+=1
    return

def onset_detect(input_file):

    y, sr = librosa.load(input_file, sr=22050)

    p = vlc.MediaPlayer(input_file)


    hop_length =512

    n_fft =2048
    onsets = librosa.onset.onset_detect(y=y,sr=sr,
                                        hop_length=hop_length)


    onset_times = librosa.frames_to_time(onsets,
                                         sr=sr,
                                         hop_length=hop_length,
                                         n_fft=n_fft)

    p.play()
    phrase_array =[]

    i, t, k = 0, 0, 0

    rhyme1 = [1, 1, 1, 0, 0]
    rhyme2 = [1, 1, 0, 0, 0]
    chorus1 = [False, 3, True, 2, rhyme1]
    chorus2 = [False, 2, False, 3, rhyme2]


    query_rhyme(query, chorus1, phrase_array)

    for arrs in phrase_array:
        print (arrs)

    arras = ["The quick brown fox", "jumps over the", "lazy dog", "Niggas in Paris", "ball so hard motherfuckers want to find me", "i j k l m ", "Whos that hoe", "Where are you bitch", "I am scared dont test me", "You disgust me", "let me in", "I shop at Amazon marketplace", "please try harder", "make me"]

    
    delta = []

    for k in range(1, len(onset_times)):
        delta.append(onset_times[i] - onset_times[k-1])


    start = time.clock()


    while (i<len(onset_times)):
        if ((time.clock()-start) >= onset_times[i]):
            i+=4
            print('beat', i)
            print (str(abs(100/int(delta[i]))+120))
            os.system("espeak " + "'" + arras[t] + "' " + "-s" + str(abs(100/int(delta[i]))+120))
            t+=1





    delta1 = []
    delta2 = []
    delta3 = []
    delta4 = []
    delta5 = []


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


def process_arguments(args):
    '''Argparse function to get the program parameters'''

    parser = argparse.ArgumentParser(
        description='librosa onset detection example')

    parser.add_argument('input_file',
                        action='store',
                        help='path to the input file (wav, mp3, etc)')

    return vars(parser.parse_args(args))


if __name__ == '__main__':
    # Get the parameters
    parameters = process_arguments(sys.argv[1:])

    # Run the beat tracker
    onset_detect(parameters['input_file'])
