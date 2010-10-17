import serial
import glob
import time

def send_message(test_fails):
    '''
    Sends a message to Arduino via serial
    '''
    arduino_usb = glob.glob('/dev/ttyUSB*')[0]
    arduino = serial.Serial(arduino_usb, 9600)
    time.sleep(1)

    if test_fails:
        arduino.write('G')
        arduino.write('R' * 10)
    else:
        arduino.write('G' * 10)
