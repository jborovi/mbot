'''
Created on May 19, 2016

@author: user
'''
from datetime import datetime

try:
    import serial
except Exception, e:
    print 'MBOT:'+str(datetime.now()) +'module searial not imported'
import time
from robot.api.common.common import Common

EMOTIONS_MAP = {'neutral':'0', 'anger':'1', 'disgust':'5', 'sadness':'4', 'fear':'2', 'scared':'2', 'joy':'3', 'sleep':'6', 'wakeup':'7'}

class AdruionConnect(object):
    '''
    Class displaying emotions on the eyes and eyebrows
    '''

    def __init__(self, dev_path, port):
        try:
            self.ser = serial.Serial(dev_path, port)
            import time
            time.sleep(2)
            self.ADRUINO_ON = True
        except Exception, e:
            self.ADRUINO_ON = False
            print 'MBOT:'+str(datetime.now()) +'module searial not imported'
            
    def close(self):
        if self.ser is not None:
            self.ser.close()        
        
    def write_emotion(self, arg):
        try:
#             print "write emo"
#             print arg
            if self.ADRUINO_ON:
#                 print 'emotion'
#                 print arg
                self.ser.write(EMOTIONS_MAP[arg])
            else:
                print 'MBOT:'+'Displaying Emotion'+arg

        except Exception, e:
            print 'MBOT:'+str(datetime.now()) + "exception in write_emotion"
            print 'MBOT:'+str(datetime.now()) + str(e)
#        self.ser.write(EMOTIONS_MAP[arg])
