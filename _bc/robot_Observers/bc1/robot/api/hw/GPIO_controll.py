'''
Created on Jun 9, 2016

@author: user
'''
import RPi.GPIO as GPIO
import time
from robot.api.common.common import Common, Event
import threading
from robot.api import Constants

class GPIO_controll(threading.Thread):
    '''
    classdocs
    '''


    debugFalseOn = False
    
    debugFalseOnStarted = None
    
    timeDebug = None
    
    button_pressed = False

    def __init__(self, pin):
        GPIO.setmode(GPIO.BCM)
        self.pin = pin
        GPIO.setup(pin,GPIO.IN)
#         
    def checkBtn(self):
#         return GPIO.input(self.pin)
        while True:
# 	    GPIO.output(self.pin,False)
  
            if (GPIO.input(self.pin)):
                Common.tty_print("Button not Pressed")
            else:
                Common.tty_print("Button pressed")
            time.sleep(1)
             
            
    def is_on(self):
#         return True  
# 	self.__check_debug_on()     
#         return self.debugFalseOn
        return not GPIO.input(self.pin)

    def __check_debug_on(self):
        import time
#         print self.debugFalseOnStarted
        
        if self.debugFalseOn:
#             print time.time() - self.debugFalseOnStarted
            if (time.time() - self.debugFalseOnStarted) > self.timeDebug:
                self.debugFalseOn=False
    
    def kill_thread(self, *args):
        print 'kill thread'
        if self.is_alive():
            self.running = False

    def setDebugFalseOnFor(self, debugForSec):
        self.debugFalseOnStarted= time.time()
        self.timeDebug = debugForSec
        self.debugFalseOn = True
        
    def run (self):
        self.running = True
        while self.running:
            if self.is_on():
                Event(Constants.EVENT_BUTTON_HOLD, Constants.EVENT_BUTTON_HOLD)
            else:
                Event(Constants.EVENT_BUTTON_HOLD, Constants.EVENT_BUTTON_NOT_HOLD)
