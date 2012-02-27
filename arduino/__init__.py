import serial
import glob
import time

def send_message(test_fails, last=False):
    '''
    Sends a message to Arduino via serial
    '''
    color = {
        True: 'R',
        False: 'G',
    }
    
    arduino_usb = glob.glob('/dev/ttyUSB*')[0]
    serial.Serial.color = lambda self, l, v: self.write(color[l]+color[v]*10)
    serial.Serial.color = lambda self, l, v: self.write(color[v])
        

    arduino = serial.Serial(arduino_usb, 9600)
    #time.sleep(1)
    arduino.color(last, test_fails)
