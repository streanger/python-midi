import time
import mido
import ctypes

import sys
import os
import ctypes
import com_ports                # to get all com's
import keyboard_translate       # to draw gui
import cv2                      # to show gui in live mode


def script_path():
    currentPath = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(currentPath)
    return currentPath
    
    
if __name__ == "__main__":
    script_path()
    names = mido.get_input_names()      # search for all ports
    outport = mido.open_output()        # port to play sound
    # outport = mido.open_output('loop1', virtual=True)        # you can try with using it and midi_loop app, to create virtual port
    print(names)
    
    # *********** GUI part ***********
    combinedTop = keyboard_translate.combine_keys_positions(top=True)
    combinedBottom = keyboard_translate.combine_keys_positions(top=False)
    image = keyboard_translate.create_blank_image(750, 1350)
    image = keyboard_translate.draw_around_keyboard(image)
    codes = []
    
    with mido.open_input(names[0], virtual=False) as inport:
        while True:
            msg = inport.receive()
            outport.send(msg)           # make sound
            print(msg)
            '''
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
            '''
        #cv2.destroyAllWindows()
