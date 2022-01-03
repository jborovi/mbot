'''
Created on May 19, 2016

@author: user
'''

import serial
import time
from robot.api.common.common import Common

EMOTIONS_MAP = {'neutral':'0', 'anger':'1', 'disgust':'5', 'sadness':'4', 'fear':'2', 'scared':'2', 'joy':'3', 'sleep':'6', 'wakeup':'7'}

class AdruionConnect(object):
    '''
    classdocs
    '''

    def __init__(self, dev_path, port):
        self.ser = serial.Serial(dev_path, port)
        
    def write_emotion(self, arg):
        try:
#             print "write emo"
#             print arg
            self.ser.write(EMOTIONS_MAP[arg])
#		self.ser.write('0')
#		time.sleep(2)
#		self.ser.write('1')
#		time.sleep(2)
#		self.ser.write('2')
#		time.sleep(2)
#		self.ser.write('3')
#		time.sleep(2)
#		self.ser.write('4')
#		time.sleep(2)
#		self.ser.write('5')

        except Exception, e:
            print e
            Common.tty_print(str(e))
#        self.ser.write(EMOTIONS_MAP[arg])
