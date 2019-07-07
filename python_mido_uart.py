import sys
import os
import time
import ctypes
import threading
import serial
import mido

import com_ports                # to get all com's
import keyboard_translate       # to draw gui
import cv2                      # to show gui in live mode


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
def cut_thing(thing, n):
    return [thing[x:x+n] for x in range(0, len(thing), n)]
    
    
def find_proper_port():
    sensorPort = '-1'
    for port, desc, hwid in sorted(com_ports.comports()):
        print("%s: %s [%s]" % (port, desc, hwid))
        if 'lightprobe' in desc.lower():
            sensorPort = port
    print()
    return sensorPort
    
    
def init_serial(com, midi):
    # com = find_proper_port()
    if midi:
        ser = serial.Serial(
            # port='COM57',
            port=com,
            baudrate=31250,     # MIDI speed
            parity=serial.PARITY_NONE,
            # stopbits=serial.STOPBITS_TWO,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            # bytesize=serial.SEVENBITS
        )
    else:
        ser = serial.Serial(
            # port='COM57',
            port=com,
            baudrate=9600,
            # baudrate=31250,
            parity=serial.PARITY_NONE,
            # stopbits=serial.STOPBITS_TWO,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
            # bytesize=serial.SEVENBITS
        )
    ser.isOpen()
    return ser
    
    
def handle_data(data):
    '''
    this functions take data, which can be convert to msg:
        command, note, velocity = data
    change name of this function to -> 'play_sound(data)'
    '''
    
    if True:
        msg = mido.parse(data)      # use parser
        outport.send(msg)           # make sound
    else:
        global notesData
        command, note, velocity = data
        
        if command == 0x90:
            noteValue = 'note_on'
            notesData.append(note)
        elif command == 0x80:
            noteValue = 'note_off'
        else:
            # think of handling other commands
            return False
            
        msg = mido.Message(noteValue, note=note, velocity=velocity)     # create message
        outport.send(msg)                                               # make sound
    return True
    
    
def read_from_port(ser, midi, quiet=False):
    ''' this function is really ugly. I need to clean it depend on midi parameter value '''
    connected = False
    # global container
    container = []
    
    # show keyboard data
    global image
    global combined
    codes = []
    while not connected:
        connected = True
        while True:
            if midi:
                reading = list(ser.read(3))
                print(reading)
                if reading[0] == 144:
                    codes.append(reading[1])
                elif reading[0] == 128:
                    codes.remove(reading[1])
                out = keyboard_translate.draw_over_image(image, combined, codes)
                cv2.imshow('out', out)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
                # think of which way is better
                if not quiet:
                    if True:
                        t = threading.Thread(target=handle_data, args=(reading,))
                        t.daemon = True
                        t.start()
                    else:
                        handle_data(reading)
            else:
                ''' not sure if this will work after changes '''
                # reading = ord(ser.read(1))
                reading = ser.read(1).decode('utf-8')
                note = convert_chars_to_notes(reading)
                container = [144, note, 127]
                if True:
                    t = threading.Thread(target=handle_data, args=(container,))
                    t.daemon = True
                    t.start()
                # reading = ser.readline()
                # print(reading, end=', ')
                print(note)
                continue
        cv2.destroyAllWindows()
    return True
    
    
def convert_chars_to_notes(character):
    ''' this function was used, when keyboard library was flashed into arduino,
        just to detect keys correctness '''
    dictio = {
        "0": 17,
        "1": 18,
        "2": 19,
        "3": 20,
        "4": 21,
        "5": 22,
        "6": 23,
        "7": 24,
        "8": 25,
        "9": 26,
        "a": 27,
        "b": 28,
        "c": 29,
        "d": 30,
        "e": 31,
        "f": 32,
        "g": 33,
        "h": 34,
        "i": 35,
        "j": 36,
        "k": 37,
        "l": 38,
        "m": 39,
        "n": 40,
        "o": 41,
        "p": 42,
        "r": 43,
        "s": 44,
        "t": 45,
        "u": 46,
        "v": 47,
        "w": 48,
        "x": 49,
        "y": 50,
        "z": 51,
        "!": 52,
        "@": 53,
        "#": 54,
        "$": 55,
        "%": 56,
        "^": 57,
        "&": 58,
        "*": 59,
        "(": 60,
        ")": 61,
        "_": 62,
        "+": 63,
        "-": 64
    }
    return dictio[character]
    
    
def notes_dictio():
    '''
        dictio key - note value
        True - on    
        False - off
    '''
    data = {key: False for key in range(21, 128)}
    return data
    
    
if __name__ == "__main__":
    script_path()
    
    # general part
    global notesData
    notesData = []
    global outport
    outport = mido.open_output()
    
    # GUI part
    global combined
    combined = keyboard_translate.combine_keys_positions()
    global image
    image = keyboard_translate.create_blank_image(400, 1350)
    image = keyboard_translate.draw_around_keyboard(image)
    
    # *********** SET MODES ***********
    midi = True     # it is used in serial initialization, and reading data
    # midi = False     # it is used in serial initialization, and reading data
    quiet = False
    
    ser = init_serial('COM3', midi)
    time.sleep(0.1)
    thread = threading.Thread(target=read_from_port, args=(ser, midi, quiet))
    # thread = threading.Thread(target=debug_read_from_port, args=(ser, midi,))     # debug
    thread.start()

    print("start to play for now")
    # while True:
        # do something here e.g. draw keyboard :)
        # time.sleep(2)
    
    
'''
pip:
    pip install mido
    pip install python-rtmidi
    
    
info:
    0x90 --> note_on
    0x80 --> note_off
    
    
package to read from MIDI device:
    https://pypi.org/project/py-midi/
    
    
tips:
    -problem with reading 7-bits data was in using function with init_serial(python side, not arduino), with wrong second parameter(True/False),
     which caused that it was always read 7-bits, not 8 as declared. In such situation value 144 goes to 17 (144-127=17)
    -cut hex to two parts:
        use divmod function, e.g.
        some = divmod(0xCDAB, 0x100)
        print(some)
        (205, 171)
        
        some = divmod(0xAB, 0x10)
        print(some)
        (10, 11)
    -
    
    
links:
    https://ccrma.stanford.edu/~craig/articles/linuxmidi/misc/essenmidi.html
    
    https://create.arduino.cc/projecthub/labsud/midi-keypad-c68fd2
    
    
    
  Command            Meaning             # parameters       param 1            param 2
    0x80             Note-off                 2               key              velocity
    0x90             Note-on                  2               key              veolcity
    0xA0            Aftertouch                2               key               touch
    0xB0      Continuous controller           2           controller #     controller value
    0xC0           Patch change               2           instrument #
    0xD0         Channel Pressure             1             pressure
    0xE0            Pitch bend                2           lsb (7 bits)       msb (7 bits)
    0xF0      (non-musical commands)
    
Furthermore, command bytes are split into half. The most significant half contains the actual MIDI command, 
and the second half contains the MIDI channel for which the command is for. For example, 
0x91 is the note-on command for the second MIDI channel. the 9 digit is the actual command for note-on 
and the digit 1 specifies the second channel (the first channel being 0). The 0xF0 set of commands do not follow this convention.    
    
    
    arduino forum:
        https://forum.arduino.cc/index.php?topic=550052.0
    
    
think of:
    -lm386 and speaker output from arduino
    -
    
    
Arduino MIDI:
    -use this library --> https://github.com/tttapa/MIDI_controller
    
    
think of this one:
    https://github.com/FortySevenEffects/arduino_midi_library/
    
    
    
    
use this values:
    http://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies
    
    
    
29.06.2019
    -can't start a new thread error
    -make some cleaning
    -think of port com
    -
    
'''





