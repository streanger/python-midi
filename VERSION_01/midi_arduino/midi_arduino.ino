/*
This is an example of the "ButtonMatrix" class of the MIDI_controller library.
Connect a 4 × 3 matrix of buttons with the rows to pins 2, 3, 4 and 5, 
and the columns to pins 6, 7 and 8.
Pull-up resistors are not necessary, because the internal ones will be used. 

If you want to be able to press multiple buttons at once, add a diode 
in series with each button, as shown in the schematic on the Wiki:
https://github.com/tttapa/MIDI_controller/wiki/Hardware

The note numbers are specified in the 'addresses' array.
Map accordingly in your DAW or DJ software.

Written by tttapa, 24/09/2017
https://github.com/tttapa/MIDI_controller
*/

#include "MIDI_Controller.h" // Include the library

// INFO --> for now there are lines to be used: 2, 13, and 0, 1, where on 1, data are transmited(MIDI OUT), and on 0, data are received(not used in real). Which means we have 3 lines, to use, but we need 4, to control full keyboard :(


/*************** PROPER CONNECTION 27.06.2019 *****************************************
 *  
 *  
 THIS IS FOR KEYPAD:
byte rowPins[ROWS] = {A4, A3, A2, A1}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {7, 6, 8, 5, 9, 4, 10, 3, 11, A0, 12, A5};    // albo 7-12, 1-6

FOR MIDI LIBRARY, ROWS SHOULD BE SWAPPED WITH COLS
 *  
 */


// channel 1
const int ROWS = 12; 
const int COLS = 4; 

byte rowPins[ROWS] = {7, 6, 8, 5, 9, 4, 10, 3, 11, A0, 12, A5};    // albo 7-12, 1-6            # 24 notes
byte colPins[COLS] = {A4, A3, A2, A1};

const uint8_t velocity = 0b1111111; // Maximum velocity (0b1111111 = 0x7F = 127)

/***** IMPORTANT THING *****
 * 
maybe it should be some change in ButtonMatrix.cpp library, in line 44:

it should be:
  uint8_t note = addresses[row][col];
instead of:
  uint8_t note = addresses[col][row];

I need to tnink for a while if this is possible to change it with using prepared functions
 * 
 * 
 */

const uint8_t addresses[ROWS][COLS] = {   // the note numbers corresponding to the buttons in the matrix
    {17, 29, 41, 53},
    {18, 30, 42, 54},
    {19, 31, 43, 55},
    {20, 32, 44, 56},
    {21, 33, 45, 57},
    {22, 34, 46, 58},
    {23, 35, 47, 59},
    {24, 36, 48, 60},
    {25, 37, 49, 61},
    {26, 38, 50, 62},
    {27, 39, 51, 63},
    {28, 40, 52, 64}
};


// Create a new instance of the class 'ButtonMatrix', called 'buttonmatrix', with dimensions 4 rows and 3 columns, with the rows connected to pins 2, 3, 4 and 5
// and the columns connected to pins 6, 7 and 8, that sends MIDI messages with the notes specified in 'addresses' on MIDI channel 1, with velocity 127
ButtonMatrix<ROWS, COLS> buttonmatrix(rowPins, colPins, addresses, 1, velocity);


void setup() {
  }

void loop() {
  // Refresh the buttons (check whether the states have changed since last time, if so, send it over MIDI)
  MIDI_Controller.refresh();
}
