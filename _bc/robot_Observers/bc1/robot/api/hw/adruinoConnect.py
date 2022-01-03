'''
Created on May 19, 2016

@author: user
'''

try:
    import serial
except Exception, e:
    print e
import time
import threading
from robot.api.common.common import Common, Observer
from robot.api import Constants

EMOTIONS_MAP = {'neutral':'0', 'anger':'1', 'disgust':'5', 'sadness':'4', 'fear':'2', 'scared':'2', 'joy':'3', 'sleep':'6', 'wakeup':'7'}

class AdruionConnect(Observer):
    '''
    classdocs
    '''

    def __init__(self, dev_path, port):
        try:
            self.ser = serial.Serial(dev_path, port)
        except Exception,e:
            print e
        Observer.__init__(self)
        
    def write_emotion(self, arg):
        try:
            print 'writing emotion'
            print arg
            self.ser.write(EMOTIONS_MAP[arg])

        except Exception, e:
            print e
            Common.tty_print(e)
#        self.ser.write(EMOTIONS_MAP[arg])

    def event_listener(self, event_name):
        print 'adr event'
        print event_name
        if event_name == Constants.EVENT_WAKE_UP:
            self.write_emotion('wake_up')
        elif event_name == Constants.EVENT_SLEEP:
            self.write_emotion('sleep')
        elif event_name == Constants.EVENT_ANGER:
            self.write_emotion('anger')
        elif event_name == Constants.EVENT_DISGUST:
            self.write_emotion('disgust')
        elif event_name == Constants.EVENT_SADNESS:
            self.write_emotion('sadness')
        elif event_name == Constants.EVENT_FEAR:
            self.write_emotion('fear')
        elif event_name == Constants.EVENT_SCARED:
            self.write_emotion('scared')
        elif event_name == Constants.EVENT_JOY:
            self.write_emotion('joy')
        elif event_name == Constants.EVENT_NEUTRAL:
            self.write_emotion('neutral')