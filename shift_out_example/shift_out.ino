#include <ShiftRegister74HC595.h>

// create a global shift register object
// parameters: (number of shift registers, data pin, clock pin, latch pin)
const byte dataPin  = 4; //Pin connected to DS of 74HC595
const byte clockPin = 3; //Pin connected to SH_CP of 74HC595
const byte latchPin = 2; //Pin connected to ST_CP of 74HC595

ShiftRegister74HC595 sr (1, dataPin, clockPin, latchPin); 


void setup() { 
}

void loop() {
  //for (int i=0; i<8; i++) {
  //  delay(250);
  //}

  // setting all pins at the same time to either HIGH or LOW
  sr.setAllHigh(); // set all pins HIGH
  delay(500);
  
  sr.setAllLow(); // set all pins LOW
  delay(500); 
  

  // setting single pins
  for (int i = 0; i < 8; i++) {
    
    sr.set(i, HIGH); // set single pin HIGH
    delay(250); 
  }
  
  
  // set all pins at once
  uint8_t pinValues[] = { B10101010 }; 
  sr.setAll(pinValues); 
  delay(1000);

  
  // read pin (zero based, i.e. 6th pin)
  uint8_t stateOfPin5 = sr.get(5);


  // set pins without immediate update
  sr.setNoUpdate(0, HIGH);
  sr.setNoUpdate(1, LOW);
  // at this point of time, pin 0 and 1 did not change yet
  sr.updateRegisters(); // update the pins to the set values

}
