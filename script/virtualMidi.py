#!/usr/bin/python3

import mido
import time

class VirtualMidi(object):

    def __init__(self, portName):
        #Create virtual midi port
        self.outPort = mido.open_output(portName, virtual=True)

    def send(self, message):
        msg = mido.Message.from_bytes(message)
        self.log(msg)
        self.outPort.send(msg)

    def log(self, msg):
        print("VirtualMidi: {}".format(msg))

if __name__ == '__main__':
    midi = VirtualMidi('Test')
    while 1:
        time.sleep(1)


