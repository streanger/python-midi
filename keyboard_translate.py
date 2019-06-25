import sys
import time
import random
import numpy as np
import cv2


def random_codes():
    codes = [random.randrange(21, 65) for x in range(5)]
    return codes
    
    
def show_image(title, image):
    '''
    WINDOW_AUTOSIZE
    WINDOW_FREERATIO
    WINDOW_FULLSCREEN
    WINDOW_GUI_EXPANDED
    WINDOW_GUI_NORMAL
    WINDOW_KEEPRATIO
    WINDOW_NORMAL
    WINDOW_OPENGL
    '''
    cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return True
    
    
def read_codes_online():
    # codes = [0x02, 0x04, 0x07, 0x14]
    codes = random_codes()
    return codes
    
    
def play_music(codes):
    # do something with codes
    print('music is playing. Just trust it', end=', ')
    return True
    
 
def combine_keys_positions():
    '''
        -this function make combined data
        -data stored in combined: posY1, posY2, posX1, posX2, color, black/white, note
        -one white key size is 250x46
        -one balck key size is 175x46    
    '''
    startNote = 21
    startX = 25
    startY = 25
    whiteColor = 230
    blackColor = 30
    
    # generate white keys
    whiteKeys = []
    for x in range(26):
        pos = (startY, startY+250, startX+x*50, startX+46+x*50, whiteColor, 'white')
        whiteKeys.append(pos)
        
    # generate black keys
    blackKeys = []
    excluded = (4, 7, 11, 14, 18, 21, 25)
    for x in range(25):
        if (x + 1) in excluded:
            pos = ()
            blackKeys.append(pos)
            continue
        pos = (startY, startY+175, startX+25+x*50, startX+42+25+x*50, blackColor, 'black')
        blackKeys.append(pos)
        
    # combined in proper way
    combinedForEnumeration = [None]*(len(whiteKeys)+len(blackKeys))
    combinedForEnumeration[::2] = whiteKeys
    combinedForEnumeration[1::2] = blackKeys
    combinedForEnumeration = [item for item in combinedForEnumeration if item]
    
    # set keys
    combinedWithKeys = [list(item) + [startNote+key] for key, item in enumerate(combinedForEnumeration)]
    
    # recombine
    whiteKeys = []
    blackKeys = []
    for item in combinedWithKeys:
        if 'white' in item:
            whiteKeys.append(item)
        else:
            blackKeys.append(item)   
    combined = tuple(whiteKeys + blackKeys)                   # black should be on the top
    return combined
    
    
def draw_over_image(image, combined, codes):
    '''
        -image --> image to be drawn over
        -codes --> codes with notes, to be highlighted
    '''
    for item in combined:
        if item:
            image[item[0]:item[1], item[2]:item[3]] = item[4]
            if item[-1] in codes:
                # item[-1] means note value
                # make some backlight for key
                # cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0), 2)
                colors = [(105, 255, 105), (255, 105, 105), (105, 105, 255)]
                color = random.choice(colors)
                cv2.rectangle(image, (item[2], item[0]), (item[3], item[1]), color, 2)
    return image
    
    
def show_keyboard():
    return True
    
    
def create_blank_image(height, width):
    image = np.zeros((height, width, 3), np.uint8)
    image += 155
    return image
    
    
if __name__ == "__main__":
    image = create_blank_image(300, 1350)
    codes = read_codes_online()             # for now generate random values
    combined = combine_keys_positions()
    out = draw_over_image(image, combined, codes)
    show_image('after drawing image', out)
    
    
    '''
    while True:
        codes = read_codes_online()
        play_music(codes)
        codes_animation(codes)
        print('codes are: {}'.format(codes))
        time.sleep(0.01)
    '''
        
        
        
'''
14.06.2019
todo:
    -read key states on raspberry
    -make some USB communication via raspberry and PC
    -play music on PC
    -draw keyboard with keys
    -if all works fine, make midi out from raspberry or arduino, which is all we need
'''

'''
combine two lists in alternating way:
https://stackoverflow.com/questions/3678869/pythonic-way-to-combine-two-lists-in-an-alternating-fashion
'''

'''
25.06.2019
todo:
    -make compatible with python_mido_uart script
    -make live mode
    
'''