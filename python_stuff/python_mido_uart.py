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
        if 'something' in desc.lower():
            sensorPort = port
    print()
    return sensorPort
    
    
def init_serial(com):
    # com = find_proper_port()
    ser = serial.Serial(
        port=com,
        baudrate=31250,     # MIDI speed
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
        # bytesize=serial.SEVENBITS
        )
    ser.isOpen()
    return ser
    
    
def handle_data(data):
    msg = mido.parse(data)      # use parser
    outport.send(msg)           # make sound
    return True
    
    
def read_from_port(port, midi, quiet=False):
    ''' this function is really ugly. I need to clean it depend on midi parameter value '''
    connected = False
    container = []
    
    
    # *********** GUI part ***********
    # combined = keyboard_translate.combine_keys_positions()
    combinedTop = keyboard_translate.combine_keys_positions(top=True)
    combinedBottom = keyboard_translate.combine_keys_positions(top=False)
    image = keyboard_translate.create_blank_image(750, 1350)
    image = keyboard_translate.draw_around_keyboard(image)
    codes = []
    
    print()
    while not connected:
        try:
            ser = init_serial(port)
            print()
            print("connection on port <{}> passed".format(port))
            connected = True
        except serial.serialutil.SerialException:
            print("connection on port <{}> is failed. Error 'serial.serialutil.SerialException' catched".format(port), end='\r', flush=True)
            # print("connection on port <{}> failed. Error 'serial.serialutil.SerialException' catched".format(port))
            time.sleep(0.2)
            continue
        while True:
            if not midi:
                try:
                    reading = list(ser.read(3))
                    reading[0]
                except:
                    connected = False
                    print("connection on port <{}> is broken. Connect device again".format(port))
                    break
                print(reading)
                if reading[0] == 144:
                    codes.append(reading[1])
                elif reading[0] == 128:
                    codes.remove(reading[1])
                out = keyboard_translate.draw_over_image(image, combinedTop, codes)
                out = keyboard_translate.draw_over_image(image, combinedBottom, codes)
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
                ''' like that just for now. Change it and clean, to be useful '''
            
                names = mido.get_input_names()      # search for all ports
                outport = mido.open_output()        # port to play sound
                # outport = mido.open_output('loop1', virtual=True)        # you can try with using it and midi_loop app, to create virtual port
                print(names)
                
                with mido.open_input(names[0], virtual=False) as inport:
                    while True:
                        msg = inport.receive()
                        outport.send(msg)           # make sound
                        print(msg)
                        
                        # get msg code
                        if msg.type == 'note_on':
                            codes.append(msg.note)
                        elif msg.type == 'note_off':
                            codes.remove(msg.note)
                        out = keyboard_translate.draw_over_image(image, combinedTop, codes)
                        out = keyboard_translate.draw_over_image(image, combinedBottom, codes)
                        cv2.imshow('out', out)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break
                            
                    cv2.destroyAllWindows()
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
    
    # *********** GENERAL PART ***********
    global notesData
    notesData = []
    global outport
    outport = mido.open_output()
    
    
    # *********** SET MODES ***********
    # midi = True     # it is used in serial initialization, and reading data
    midi = False     # it is used in serial initialization, and reading data
    quiet = False
    
    
    thread = threading.Thread(target=read_from_port, args=('COM3', midi, quiet))
    thread.start()

    # *********** DO SOMETHING HERE ***********
    
    
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
    
14.07.2019
    -functionalities from apps "python_mido_uart.py" and "python_mido_usb.py" should be in switchable in one application
    
'''
