#!/usr/bin/python3

import mido
import time
from serialParser import SerialParser
from virtualMidi import VirtualMidi

if __name__ == '__main__':
    parser = SerialParser('/dev/ttyUSB2', 115200, 1)
    midi = VirtualMidi('BioMidi')
    while 1:
        incoming_messages = parser.read()
        if(incoming_messages):
            parsed_messages = parser.parse(incoming_messages)
            print(parsed_messages)
            if not len(parsed_messages):
                continue

            for message in parsed_messages:
                midi.send(message)

        time.sleep(0.01)
