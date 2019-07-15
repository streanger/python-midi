import sys
import time
import mido
import ctypes


def data(key):
    ''' midi notes '''
    some = {
        'C0': 12,
        'D0': 14,
        'E0': 16,
        'F0': 17,
        'G0': 19,
        'A0': 21,
        'B0': 23,
        
        'C1': 24,
        'D1': 26,
        'E1': 28,
        'F1': 29,
        'G1': 31,
        'A1': 33,
        'B1': 35,
        
        'C2': 36,
        'D2': 38,
        'E2': 40,
        'F2': 41,
        'G2': 43,
        'A2': 45,
        'B2': 47,
        
        'C3': 48,
        'D3': 50,
        'E3': 52,
        'F3': 53,
        'G3': 55,
        'A3': 57,
        'B3': 59,
        
        'C4': 60,
        'D4': 62,
        'E4': 64,
        'F4': 65,
        'G4': 67,
        'A4': 69,
        'B4': 71,
        
        'C5': 72,
        'D5': 74,
        'E5': 76,
        'F5': 77,
        'G5': 79,
        'A5': 81,
        'B5': 83,
        
        'C6': 84,
        'D6': 86,
        'E6': 88,
        'F6': 89,
        'G6': 91,
        'A6': 93,
        'B6': 95,
        
        'C7': 96,
        'D7': 98,
        'E7': 100,
        'F7': 101,
        'G7': 103,
        'A7': 105,
        'B7': 107,
        
        'C8': 108,
        'D8': 110,
        'E8': 112,
        'F8': 113,
        'G8': 115,
        'A8': 117,
        'B8': 119,
    }
    return some[key]
    
    
def wait_time(key):
    ''' timing for notes '''
    s1 = 0.320
    # s1 = 0.250
    s2 = 2*s1
    s3 = 3*s1
    s4 = 4*s1
    data = {
        's1': s1,
        's2': s2,
        's3': s3,
        's4': s4,
    }
    return data[key]
    
    
def songs(key):
    ''' songs stored in my format :) '''
    data = {
    'hallelujah':
        [('E5', 's1'), ('G5', 's2'), ('G5', 's1'), ('G5', 's2'), ('G5', 's1'), ('A5', 's1'), ('A5', 's1'), ('A5', 's3'),
         ('E5', 's1'), ('G5', 's2'), ('G5', 's1'), ('G5', 's2'), ('G5', 's1'), ('A5', 's1'), ('A5', 's1'), ('A5', 's3'),
         ('G5', 's1'), ('A5', 's2'), ('A5', 's2'), ('A5', 's1'), ('A5', 's1'), ('A5', 's2'),
         ('G5', 's1'), ('G5', 's2'), ('F5', 's1'), ('G5', 's3'), ('G5', 's3'),
         ('XX', 's4'),
         ('E5', 's1'), ('G5', 's2'), ('G5', 's1'), ('G5', 's2'), ('G5', 's1'), ('A5', 's2'), ('A5', 's1'), ('B5', 's2'),
         ('G5', 's1'), ('C6', 's2'), ('C6', 's1'), ('C6', 's2'), ('C6', 's1'), ('C6', 's2'), ('C6', 's1'), ('D6', 's2'),
         ('C6', 's1'), ('D6', 's2'), ('D6', 's3'), ('D6', 's1'), ('D6', 's1'), ('E6', 's3'), ('E6', 's2'), ('D6', 's1'), ('D6', 's3'), ('C6', 's4'),
         ('E5', 's2'), ('G5', 's1'), ('A5', 's3'), ('A5', 's4'),
         ('A5', 's2'), ('G5', 's1'), ('E5', 's3'), ('E5', 's4'),
         ('E5', 's2'), ('G5', 's1'), ('A5', 's3'), ('A5', 's4'),
         ('A5', 's2'), ('G5', 's1'), ('E5', 's2'), ('F5', 's2'), ('E5', 's1'), ('D5', 's4'), ('C5', 's1'), ('C5', 's3')
         ],
    
    'some':
        [('E5', 's2'), ('G5', 's1'), ('A5', 's3'), ('A5', 's4'),
         ('A5', 's2'), ('G5', 's1'), ('E5', 's3'), ('E5', 's4')]
    }
    return data[key]
    
    
def limited(value):
    ''' edges are 0 and 8 '''
    if value < 0:
        return 0
    elif value > 8:
        return 0
    else:
        return value
        
        
def move_tone(song, diff):
    ''' move tone up/down. All tones values are limited by 0 and 8 '''
    out = [(key[0] + str(limited(int(key[1]) + diff)), value) if (not key == 'XX') else (key, value) for key, value in song]
    return out
    
    
def play_song(song):
    ''' play song in my format, by sending msg note_on, waiting, and sending note_off '''
    for key, value in song:
        print("note: {}, timing: {}".format(key, value), end='\r', flush=True)
        if key == 'XX':
            time.sleep(wait_time(value))
            continue
        msg = mido.Message('note_on', note=data(key))
        outport.send(msg)
        codes = [data(key)]     # for now one note at the time
        time.sleep(wait_time(value))
        msg = mido.Message('note_off', note=data(key))
        outport.send(msg)
    return True
    
    
if __name__ == "__main__":
    # names = mido.get_input_names()      # search for all ports
    outport = mido.open_output()        # port to play sound
    
    song = songs('hallelujah')
    song = move_tone(song, -1)       # two tones up
    play_song(song)
    
    
'''
todo:
    -make some converter app
    -make gui with keys
    -
    
'''
