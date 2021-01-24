#!/usr/bin/python3

import serial

class SerialParser(object):
    INCOMING_BUFFER_MIN_SIZE = 5

    def __init__(self, port, baudrate, timeout, stub=False):
        if not stub:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)

    def read(self):
        incoming_bytes = []
        input_buffer_len = self.ser.in_waiting
        if input_buffer_len:
            for i in range(input_buffer_len):
                incoming_bytes.append(int.from_bytes(self.ser.read(),byteorder='little'))

        return incoming_bytes

    def parse(self, buffer):
        midi_messages_list = []
        if len(buffer) < self.INCOMING_BUFFER_MIN_SIZE:
            self.log("Buffer lenght is too small")
            return []

        if (len(buffer) - 1) % 4:
            self.log("Buffer lenght is not multiple of 4")
            return []

        number_of_midi_messages = int((len(buffer) - 1)/4)
        print(buffer)
        # The first 2 bytes of the buffer are timestamps
        single_midi_message = []
        try:
            del buffer[0:1]
        except Exception as e:
            self.log(e)

        for i in range(number_of_midi_messages):
            midi_messages_list.append(buffer[1+i*4:4 + i*4])

        return midi_messages_list

    def log(self, msg):
        print("SerialParser: {}".format(msg))


