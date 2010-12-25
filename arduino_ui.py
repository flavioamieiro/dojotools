#-*- coding: utf-8 -*-
"""


Dojotools - tools for your coding dojo session

Copyright (C) 2009 Flávio Amieiro <amieiro.flavio@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; version 2 dated June, 1991.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Library General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

If you find any bugs or have any suggestions email: amieiro.flavio@gmail.com
"""
import sys
import glob

try:
    import firmata
except ImportError:
    sys.stderr.write("""Could not find the firmata module.\nIn order to use the arduino as an output you need to install it.\nGo to https://github.com/lupeke/python-firmata for more information on how to install python-firmata\n""")
    sys.exit(1)

class ArduinoUi(object):
    # we need to add timer functionality to this ui.  I'll wait until
    # I fix the gtk dependency, because that will probably change the
    # way we count the time.

    RED_PIN = 7
    GREEN_PIN = 8

    def __init__(self):
        try:
            arduino_path = glob.glob('/dev/ttyUSB*')[0]
        except IndexError:
            sys.stderr.write("""Could not find an arduino device. Looked for /dev/ttyUSB*\nCheck if the arduino is plugged in, and that you have the right permissions.\n""")
            sys.exit(1)

        self.arduino = firmata.Arduino(arduino_path)

        self.arduino.pin_mode(self.GREEN_PIN, firmata.OUTPUT)
        self.arduino.pin_mode(self.RED_PIN, firmata.OUTPUT)

    def show_command_results(self, status, output):
        # we still need to show the output in the terminal
        # window.
        sys.stdout.write(output)

        if status == 0:
            pin_to_light_up = self.GREEN_PIN
            pin_to_dim = self.RED_PIN
        else:
            pin_to_light_up = self.RED_PIN
            pin_to_dim = self.GREEN_PIN

        self.arduino.digital_write(pin_to_light_up, firmata.HIGH)
        self.arduino.digital_write(pin_to_dim, firmata.LOW)
