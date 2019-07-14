#include "MIDI_Controller.h" // Include the library

// 13.07.2019

/*
                        ATMEL ATmega32
             
                            +---\\---+
       (XCK/T0) D0 PB0  01|        |40  PA0 AI7 D31 (ADC0)
           (T1) D1 PB1  02|        |39  PA1 AI6 D30 (ADC1)
    (INT2/AIN0) D2 PB2  03|        |38  PA2 AI5 D29 (ADC2)
     (OC0/AIN1) D3 PB3  04|        |37  PA3 AI4 D28 (ADC3)
           (SS) D4 PB4  05|        |36  PA4 AI3 D27 (ADC4)
         (MOSI) D5 PB5  06|        |35  PA5 AI2 D26 (ADC5)
         (MISO) D6 PB6  07|        |34  PA6 AI1 D25 (ADC6)
          (SCK) D7 PB7  08|        |33  PA7 AI0 D24 (ADC7)
                 RESET  09|        |32  AREF
                   VCC  10|        |31  GND
                   GND  11|        |30  AVCC
                 XTAL2  12|        |29  PC7 D23 (TOSC2)
                 XTAL1  13|        |28  PC6 D22 (TOSC1)
          (RXD) D8 PD0  14|        |27  PC5 D21 (TDI)
          (TXD) D9 PD1  15|        |26  PC4 D20 (TDO)
        (INT0) D10 PD2  16|        |25  PC3 D19 (TMS)
        (INT1) D11 PD3  17|        |24  PC2 D18 (TCK)
        (OC1B) D12 PD4  18|        |23  PC1 D17 (SDA)
        (OC1A) D13 PD5  19|        |22  PC0 D16 (SCL)
        (ICP1) D14 PD6  20|        |21  PD7 D15 (OC2)
                          +--------+
*/


// 4 pins of C port are blocked by JTAG
//MCUCSR = (1<<JTD);
//MCUCSR = (1<<JTD);

const int ROWS = 12; 
const int COLS = 8; 

byte rowPins[ROWS] = {1, 7, 2, 11, 3, 12, 4, 13, 5, 14, 6, 10};
byte colPins[COLS] = {27, 26, 25, 24, 31, 30, 29, 28};
const uint8_t velocity = 0b1111111; // Maximum velocity (0b1111111 = 0x7F = 127)


const uint8_t addresses[ROWS][COLS] = {   // the note numbers corresponding to the buttons in the matrix
    {25, 37, 49, 61, 73, 85, 97, 109},
    {26, 38, 50, 62, 74, 86, 98, 110},
    {27, 39, 51, 63, 75, 87, 99, 111},
    {28, 40, 52, 64, 76, 88, 100, 112},
    {29, 41, 53, 65, 77, 89, 101, 113},
    {30, 42, 54, 66, 78, 90, 102, 114},
    {31, 43, 55, 67, 79, 91, 103, 115},
    {32, 44, 56, 68, 80, 92, 104, 116},
    {33, 45, 57, 69, 81, 93, 105, 117},
    {34, 46, 58, 70, 82, 94, 106, 118},
    {35, 47, 59, 71, 83, 95, 107, 119},
    {36, 48, 60, 72, 84, 96, 108, 120}
};


/* 
    {17, 29, 41, 53, 65, 77, 89, 101},
    {18, 30, 42, 54, 66, 78, 90, 102},
    {19, 31, 43, 55, 67, 79, 91, 103},
    {20, 32, 44, 56, 68, 80, 92, 104},
    {21, 33, 45, 57, 69, 81, 93, 105},
    {22, 34, 46, 58, 70, 82, 94, 106},
    {23, 35, 47, 59, 71, 83, 95, 107},
    {24, 36, 48, 60, 72, 84, 96, 108},
    {25, 37, 49, 61, 73, 85, 97, 109},
    {26, 38, 50, 62, 74, 86, 98, 110},
    {27, 39, 51, 63, 75, 87, 99, 111},
    {28, 40, 52, 64, 76, 88, 100, 112}
};
*/

ButtonMatrix<ROWS, COLS> buttonmatrix(rowPins, colPins, addresses, 1, velocity);

void setup() {
}

void loop() {
  // Refresh the buttons (check whether the states have changed since last time, if so, send it over MIDI)
  MIDI_Controller.refresh();
}
