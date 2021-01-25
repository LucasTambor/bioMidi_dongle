#!/usr/bin/python3

import argparse
import time
from serialParser import SerialParser
from virtualMidi import VirtualMidi

class BioMidiCli(object):
    def __init__(self, bioMidi):
        self.bioMidi = bioMidi
        self.parser = self._get_parser()

    def run(self):
        try:
            args = self.parser.parse_args()
            args.func(args)
        except Exception as failure:
            print("Error: {}".format(str(failure)))

    def _get_parser(self):
        parser_top = argparse.ArgumentParser(description='BioMidi cli tool')

        subparsers = parser_top.add_subparsers()

        # Run Command
        parser_run = subparsers.add_parser('run', help='Run BioMidi')
        parser_run.add_argument('-p', '--port', required=True, help="USB Port for BioMidiDongle")
        parser_run.add_argument('-b', '--baud', required=True, type=int, help="USB Port BaudRate")
        parser_run.add_argument('-t', '--timeout', default=1, type=int, help="USB Port Timeout")
        parser_run.set_defaults(func=self._cmd_run)

        # Map Command
        parser_map = subparsers.add_parser('map', help='Map control message to DAW')
        parser_map.set_defaults(func=self._cmd_map)

        # Test Command
        parser_test = subparsers.add_parser('test', help='Test control message to DAW')

        parser_test.set_defaults(func=self._cmd_test)

        return parser_top

    def _cmd_run(self, args):
        self.serialParser = SerialParser(args.port, args.baud, args.timeout)
        while 1:
            incoming_messages = self.serialParser.read()
            if(incoming_messages):
                parsed_messages = self.serialParser.parse(incoming_messages)
                print(parsed_messages)
                if not len(parsed_messages):
                    continue

                for message in parsed_messages:
                    try:
                        self.bioMidi.send(message)
                    except Exception as e:
                        print(e)

    def _cmd_map(self, args):
        execute = 1
        while execute:
            command = int(input("Control: "), 16)
            if not command:
                execute = 0
                return
            self.bioMidi.send([186, command, 0])

    def _cmd_test(self, args):
        execute = 1
        while execute:
            command = int(input("Control: "), 16)
            value = int(input("Value: "))
            if not command:
                execute = 0
            self.bioMidi.send([186, command, value])

if __name__ == '__main__':

    parser = SerialParser('/dev/ttyUSB2', 115200, 1)
    midi = VirtualMidi('BioMidi')
    cli = BioMidiCli(midi)

    cli.run()
