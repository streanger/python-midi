#include <Keypad.h>

/******************* DEFINED DATA *******************/
#define NOTE_VELOCITY 100


/******************* MIDI MODE *******************/
//boolean midiMode = false;      // if midiMode = false, the Arduino will send on and off messages via the serial monitor.
boolean midiMode = true;        // if midiMode = true, the Arduino will act as a native MIDI device.


boolean buttonState04 = LOW;
boolean buttonState05 = LOW;
boolean buttonState06 = LOW;
boolean buttonState07 = LOW;


/******************* KEYBOARD *******************/
// define keyboard variables here

const byte ROWS = 12; 
const byte COLS = 4; 

char hexaKeys[ROWS][COLS] = {
  {'1CFD1', '2CFD1', '3CFD1', '4CFD1'},
  {'1F1', '2D1', '3D1', '4D1'},
  {'1G1', '2DBE1', '3DBE1', '4DBE1'},
  {'1BE1', '2BE1', '3BE1', '4BE1'},
  {'1CF1', '2CF1', '3CF1', '4CF1'},
  {'1CFG1', '2CFG1', '3CFG1', '4CFG1'},
  {'1G1', '2G1', '3G1', '4G1'},
  {'1GA1', '2GA1', '3GA1', '4GA1'},
  {'1A1', '2A1', '3A1', '4A1'},
  {'1ABE1', '2ABE1', '3ABE1', '4ABE1'},
  {'1BE2', '2BE2', '3BE2', '4BE2'},
  {'1CF2', '2CF2', '3CF2', '4CF2'}
};

byte rowPins[ROWS] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12};    // albo 7-12, 1-6
byte colPins[COLS] = {A1, A2, A3, A4}; 

Keypad kpd = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS);

String msg = "";

//________________________________________________________________________________________________________________________________________
void setup() {
  if (midiMode) {
    Serial.begin(31250); // this is the standard communication baudrate for MIDI devices, do not change this!
  }
  else {
    Serial.begin(9600);
    //Serial.begin(31250);
  }
  
  pinMode(4, INPUT_PULLUP);
  pinMode(5, INPUT_PULLUP);
  pinMode(6, INPUT_PULLUP);
  pinMode(7, INPUT_PULLUP);
  
}

//________________________________________________________________________________________________________________________________________
void loop() {
  /*
  sendMidi(0x90, 4, 64);
  for (uint8_t i = 21; i <= 108; i++) {
     sendMidi(0x90, i, 64);
     delay(100);
     sendMidi(0x80, i, 64);
  }*/
  
  
  // this one propably won't be used
  /*
  // Fills kpd.key[ ] array with up-to 10 active keys.
  // Returns true if there are ANY active keys.
  if (kpd.getKeys())
  {
      for (int i=0; i<LIST_MAX; i++)   // Scan the whole key list.
      {
          if ( kpd.key[i].stateChanged )   // Only find keys that have changed state.
          {
              switch (kpd.key[i].kstate) {  // Report active key state : IDLE, PRESSED, HOLD, or RELEASED
                  case PRESSED:
                  msg = " PRESSED.";
              break;
                  case HOLD:
                  msg = " HOLD.";
              break;
                  case RELEASED:
                  msg = " RELEASED.";
              break;
                  case IDLE:
                  msg = " IDLE.";
              }
              Serial.print("Key ");
              Serial.print(kpd.key[i].kchar);
              Serial.println(msg);
          }
      }
  }
  */

  
  // very random midi note
  buttonState04 = digitalRead(4);
  buttonState05 = digitalRead(5);
  buttonState06 = digitalRead(6);
  buttonState07 = digitalRead(7);
  
  if (buttonState04 == LOW) {
    sendMidi(0x90, 50, NOTE_VELOCITY);
  } else {
    sendMidi(0x80, 50, NOTE_VELOCITY);
  }
  
  if (buttonState05 == LOW) {
    sendMidi(0x90, 52, NOTE_VELOCITY);
  } else {
    sendMidi(0x80, 52, NOTE_VELOCITY);
  }
  
  if (buttonState06 == LOW) {
    sendMidi(0x90, 54, NOTE_VELOCITY);
  } else {
    sendMidi(0x80, 54, NOTE_VELOCITY);
  }
  
  if (buttonState07 == LOW) {
    sendMidi(0x90, 56, NOTE_VELOCITY);
  }
  else {
    sendMidi(0x80, 56, NOTE_VELOCITY);
  }
  
  
  
}


//________________________________________________________________________________________________________________________________________
void sendMidi(uint8_t statusbyte, uint8_t databyte1, uint8_t databyte2) {
  if (midiMode) {
    Serial.write(statusbyte); //send noteOn, noteOff or Control Change command
    Serial.write(databyte1); //send pitch or channel data
    Serial.write(databyte2); //send velocity/ value data
  }
  else {
    Serial.print(statusbyte);
    Serial.print(" ");
    Serial.print(databyte1);
    Serial.print(" ");
    Serial.println(databyte2);
  }
}


/*
void sendMIDI(uint8_t messageType, uint8_t channel, uint8_t data1, uint8_t data2) {
  // from --> https://tttapa.github.io/Arduino/MIDI/Chap03-MIDI-over-Serial.html
  channel--;                                   // Decrement the channel, because MIDI channel 1 
                                               // corresponds to binary channel 0
  messageType &= 0b11110000;                   // Make sure that only the high nibble 
                                               // of the message type is set
  channel     &= 0b00001111;                   // Make sure that only the low nibble
                                               // of the channel is set
  uint8_t statusByte = messageType | channel;  // Combine the messageType (high nibble) 
                                               // with the channel (low nibble)
                                               // Both the message type and the channel
                                               // should be 4 bits wide
  statusByte  |= 0b10000000;                   // Set the most significant bit of the status byte
  data1       &= 0b01111111;                   // Clear the most significant bit of the data bytes
  data2       &= 0b01111111;
  Serial.write(statusByte);                    // Send over Serial
  Serial.write(data1);
  Serial.write(data2);
}*/



/*
Klawisze 1-12 -> piny 1-12 (nie ma pewności, co do kolejności połówek, tj 1-6 -> 7-12, 7-12 -> 1-6)
Rzędy 1-4 -> piny A1-A4

44 klawisze na jednej klawiaturze
1 klawiatura:
  4*12 -> 4+12 -> 16 pinów
2 klawiatury:
  8*12 -> 8+12 -> 20 pinów

*/

