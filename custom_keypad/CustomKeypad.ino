/* @file CustomKeypad.pde
|| @version 1.0
|| @author Alexander Brevig
|| @contact alexanderbrevig@gmail.com
||
|| @description
|| | Demonstrates changing the keypad size and key values.
|| #
*/
#include <Keypad.h>

const byte ROWS = 4; //four rows
const byte COLS = 12; //four columns
//define the cymbols on the buttons of the keypads
const uint8_t hexaKeys[ROWS][COLS] = {
    {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b'},
    {'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'},
    {'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!'},
    {'@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-'}
};

/*
    {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b'},
    {'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'},
    {'o', 'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!'},
    {'@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-'}
};


    {21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32},
    {33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44},
    {45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56},
    {57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68}
};
 */


byte rowPins[ROWS] = {A4, A3, A2, A1}; //connect to the row pinouts of the keypad
//byte colPins[COLS] = {A0, A5, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}; //connect to the column pinouts of the keypad
byte colPins[COLS] = {7, 6, 8, 5, 9, 4, 10, 3, 11, A0, 12, A5};    // albo 7-12, 1-6


//initialize an instance of class NewKeypad
Keypad customKeypad = Keypad( makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  Serial.begin(9600);
}
  
void loop(){
  char customKey = customKeypad.getKey();
  
  if (customKey){
    //Serial.println(customKey);
    Serial.write(customKey);
  }
}
