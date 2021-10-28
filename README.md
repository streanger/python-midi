# python_midi
My struggles with MIDI, with using arduino and python

## versions - each of them is different type

### VERSION_01
  - description: *first way is to create python app, which can read from UART(arduino or something), and play sounds. It can be some GUI for that*
  - board: arduino unoR3 clone
  - lib: MIDI_controller (https://github.com/tttapa/MIDI_controller)
  - out: fake MIDI (UART)
  - audio app: python app --> python_mido_uart.py
  - keys number: 44 (12*4 - 4) (half of the keyboard)
  - GUI: False
  
![image](VERSION_01/arduino_midi_bb.png)
  
### VERSION_02

  - description: *second way is to create arduino which works as MIDI device and sends data over USB*
  - to be done
  
### VERSION_03

  - description: *third way is to create arduino with MIDI connector and bypass it over MIDI-USB switch to PC. It can also works over UART, using FTDI*
  - board: atmega32
  - lib: MIDI_controller (https://github.com/tttapa/MIDI_controller)
  - out: fake MIDI (UART) / MIDI connector
  - audio app: python app --> python_mido_uart.py / specified_midi_app
  - keys number: 88 (12*8 - 8; 2x 44-keys-keyboard; can handle 96 in this configuration)
  - GUI: True (python_mido_uart.py / specified_midi_app)
  
### VERSION_04

  - description: *fourth way is to create binding for dll(loop_midi etc) in python*
  - to be done
  
  
## GUI - keyboard visualisation

![image](keyboard_gui.png)
