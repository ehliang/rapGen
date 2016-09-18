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
from espeak import ESpeak
import os
import wave
from textstat.textstat import textstat
from set_parse_tree import MarkovModel as mm
from pydub import AudioSegment

def query_rhyme(query, mylist, phrase_array):
    set1 = query(mylist[1], mylist[0])
    set2 = query(mylist[3], mylist[2])

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

    rhymegen = mm()

    es = ESpeak()

    if os.path.isfile('./overlaid.wav'):
        os.remove('./overlaid.wav')

    file_list = os.listdir("./wav")

    file_list.sort(key=float)

    for file in file_list:
        os.remove('./wav/'+ file)

    delta = []

    

    y, sr = librosa.load(input_file, sr=22050)

    #p = vlc.MediaPlayer(input_file)


    hop_length =512

    n_fft =2048
    onsets = librosa.onset.onset_detect(y=y,sr=sr,
                                        hop_length=hop_length)


    onset_times = librosa.frames_to_time(onsets,
                                         sr=sr,
                                         hop_length=hop_length,
                                         n_fft=n_fft)

    #p.play()
    phrase_array =[]

    i, t, k = 0, 0, 0

    c_rhyme1 = [1, 1, 1, 0, 0]
    c_rhyme2 = [1, 1, 0, 0, 0]
    c_rhyme3 = [1, 0, 1, 0, 1]
    c_rhyme4 = [1, 1, 0, 0, 1]

    v_rhyme1 = [1, 1, 0, 0]
    v_rhyme2 = [1, 0, 1, 0]
    v_rhyme3 = [1, 0, 0, 1]


    chorus1 = [False, 3, True, 2, c_rhyme1]
    chorus1 = [False, 2, False, 3, c_rhyme2]
    chorus2 = [False, 2, False, 3, c_rhyme2]


    



    query_rhyme(rhymegen.generate_rhymes, chorus1, phrase_array)
    query_rhyme(rhymegen.generate_rhymes, chorus2, phrase_array)



    #phrase_array = ["The quick brown fox", "jumps over the", "lazy dog", "Niggas in Paris", "ball so hard motherfuckers want to find me", "i j k l m ", "Whos that hoe"]
    
    for arrs in phrase_array:
        print (arrs)

    for k in range(1, len(onset_times)):
        delta.append(onset_times[k] - onset_times[k-1])


    start = time.clock()

    n=0


    while (n<len(onset_times)):
        if ((time.clock()-start) >= onset_times[n]):
            print('beat', n)
            #es.speed=float(abs(100/int(delta[i]))+120)
            if t<len(phrase_array):
                es.args['speed'][1]=int(abs(1/delta[n])*7+190)
                es.save(phrase_array[t],'./wav/'+(str(onset_times[n])))
                es.say(phrase_array[t])
                n+=(int(textstat.syllable_count(phrase_array[t])))
                time.sleep(2)
                #os.system("espeak " + "'" + arras[t] + "' " + "-s" + str(int(abs(1/delta[n])+140))) 
                t+=1
            else:
                n=3500000

    sound1 = AudioSegment.from_wav('./rap.wav')



    for file in file_list:
            the_wave = AudioSegment.from_wav('./wav/'+ file)
            sound_with_wave = sound1.overlay(the_wave, position=int(float(file)*1000))
            print (float(file)*1000)
            sound_with_wave.export('overlaid.wav', format='wav')
            sound1 = AudioSegment.from_wav('./overlaid.wav')




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
