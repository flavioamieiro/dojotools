import serial
import glob

def send_message(message):
    '''
    Sends a message to Arduino via serial
    '''
    arduino_usb = glob.glob('/dev/ttyUSB*')[0]
    arduino = serial.Serial(arduino_usb, 9600)
    arduino.timeout = 0.1
    arduino.write(message)
    arduino.close()
