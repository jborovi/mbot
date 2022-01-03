'''
Created on May 19, 2016

@author: user
'''

import serial
import time

EMOTIONS_MAP = {'neutral':'0', 'anger':'1', 'disgust':'1', 'sadness':'4', 'fear':'2', 'scared':'2', 'scared':'2', 'joy':'3', 'sleep':'5'}

class AdruionConnect(object):
    '''
    classdocs
    '''

    def __init__(self, dev_path, port):
        self.ser = serial.Serial(dev_path, port)
        
    def write_emotion(self, arg):
	try:
		print arg
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
		print 'aaa'
		print e
		print 'Exc in adruion'
#        self.ser.write(EMOTIONS_MAP[arg])
